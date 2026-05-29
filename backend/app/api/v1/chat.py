"""在线客服/聊天API"""
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.response import success_response, error_response
from app.models.chat import ChatSession, ChatMessage, QuickReply
from app.models.user import User
from app.api.v1.deps import get_current_user

router = APIRouter()


class SendMessageRequest(BaseModel):
    content: str
    message_type: str = "text"


def _format_time(value):
    return value.strftime("%Y-%m-%d %H:%M:%S") if value else None


def _serialize_message(message: ChatMessage) -> dict:
    return {
        "id": message.id,
        "sender_type": message.sender_type,
        "sender_id": message.sender_id,
        "content": message.content,
        "message_type": message.message_type,
        "is_read": message.is_read,
        "created_at": _format_time(message.created_at),
    }


def _get_active_session(db: Session, user_id: int) -> ChatSession:
    return db.query(ChatSession).filter(
        ChatSession.user_id == user_id,
        ChatSession.status == "active"
    ).order_by(ChatSession.updated_at.desc()).first()


def _get_latest_session(db: Session, user_id: int) -> ChatSession:
    return db.query(ChatSession).filter(
        ChatSession.user_id == user_id
    ).order_by(ChatSession.updated_at.desc(), ChatSession.id.desc()).first()


def _create_session(db: Session, user_id: int) -> ChatSession:
    session = ChatSession(user_id=user_id, status="active")
    db.add(session)
    db.commit()
    db.refresh(session)

    welcome_msg = ChatMessage(
        session_id=session.id,
        sender_type="system",
        content="您好！欢迎咨询博才科研百测。请直接描述您的问题，后台客服会为您回复。",
        message_type="text",
        is_read=False,
    )
    db.add(welcome_msg)
    session.updated_at = datetime.now()
    db.commit()
    db.refresh(session)
    return session


@router.get("/session")
async def get_or_create_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取或创建聊天会话"""
    session = _get_active_session(db, current_user.id)
    if not session:
        session = _get_latest_session(db, current_user.id) or _create_session(db, current_user.id)

    return success_response(data={
        "session_id": session.id,
        "status": session.status,
        "created_at": _format_time(session.created_at)
    })


@router.get("/history")
async def get_chat_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取聊天记录"""
    session = _get_active_session(db, current_user.id) or _get_latest_session(db, current_user.id)
    if not session:
        return success_response(data={"items": [], "total": 0})

    query = db.query(ChatMessage).filter(ChatMessage.session_id == session.id)
    total = query.count()

    # 获取最新消息
    messages = query.order_by(ChatMessage.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    messages.reverse()  # 按时间正序返回

    unread_staff_messages = [
        message for message in messages
        if message.sender_type in ("staff", "system") and not message.is_read
    ]
    for message in unread_staff_messages:
        message.is_read = True
    if unread_staff_messages:
        db.commit()

    return success_response(data={
        "items": [_serialize_message(m) for m in messages],
        "total": total,
        "session_id": session.id
    })


@router.post("/send")
async def send_message(
    request: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发送消息，等待后台客服真实回复"""
    content = (request.content or "").strip()
    if not content:
        return error_response(message="请输入消息内容")

    session = _get_active_session(db, current_user.id)
    if not session:
        session = _create_session(db, current_user.id)

    # 保存用户消息
    user_message = ChatMessage(
        session_id=session.id,
        sender_type="user",
        sender_id=current_user.id,
        content=content,
        message_type=request.message_type,
        is_read=False,
    )
    db.add(user_message)
    session.status = "active"
    session.updated_at = datetime.now()
    db.commit()
    db.refresh(user_message)

    return success_response(data={
        "session_id": session.id,
        "message_id": user_message.id,
        "created_at": _format_time(user_message.created_at),
        "waiting_reply": True
    }, message="消息已发送")


@router.get("/quick-replies")
async def get_quick_replies(
    db: Session = Depends(get_db)
):
    """获取快捷问题列表"""
    replies = db.query(QuickReply).filter(
        QuickReply.is_active == True
    ).order_by(QuickReply.sort_order.asc()).all()
    
    return success_response(data={
        "items": [
            {
                "id": r.id,
                "question": r.question,
                "category": r.category
            }
            for r in replies
        ]
    })


@router.post("/session/close")
async def close_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """关闭会话"""
    session = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatSession.status == "active"
    ).first()
    
    if session:
        session.status = "closed"
        session.closed_at = datetime.now()
        session.updated_at = datetime.now()
        db.commit()
    
    return success_response(message="会话已关闭")
