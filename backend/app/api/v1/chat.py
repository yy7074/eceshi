"""在线客服/聊天API"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
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


@router.get("/session")
async def get_or_create_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取或创建聊天会话"""
    # 查找活跃会话
    session = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatSession.status == "active"
    ).first()
    
    if not session:
        # 创建新会话
        session = ChatSession(
            user_id=current_user.id,
            status="active"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        # 发送欢迎消息
        welcome_msg = ChatMessage(
            session_id=session.id,
            sender_type="system",
            content="您好！欢迎使用在线客服，请问有什么可以帮助您的？",
            message_type="text"
        )
        db.add(welcome_msg)
        db.commit()
    
    return success_response(data={
        "session_id": session.id,
        "status": session.status,
        "created_at": session.created_at.strftime("%Y-%m-%d %H:%M:%S") if session.created_at else None
    })


@router.get("/history")
async def get_chat_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取聊天记录"""
    # 获取活跃会话
    session = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatSession.status == "active"
    ).first()
    
    if not session:
        return success_response(data={"items": [], "total": 0})
    
    query = db.query(ChatMessage).filter(ChatMessage.session_id == session.id)
    total = query.count()
    
    # 获取最新消息
    messages = query.order_by(ChatMessage.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    messages.reverse()  # 按时间正序返回
    
    return success_response(data={
        "items": [
            {
                "id": m.id,
                "sender_type": m.sender_type,
                "content": m.content,
                "message_type": m.message_type,
                "is_read": m.is_read,
                "created_at": m.created_at.strftime("%Y-%m-%d %H:%M:%S") if m.created_at else None
            }
            for m in messages
        ],
        "total": total,
        "session_id": session.id
    })


@router.post("/send")
async def send_message(
    request: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发送消息"""
    # 获取或创建会话
    session = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatSession.status == "active"
    ).first()
    
    if not session:
        session = ChatSession(user_id=current_user.id, status="active")
        db.add(session)
        db.commit()
        db.refresh(session)
    
    # 保存用户消息
    user_message = ChatMessage(
        session_id=session.id,
        sender_type="user",
        sender_id=current_user.id,
        content=request.content,
        message_type=request.message_type
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    # 自动回复（简单关键词匹配）
    auto_reply = get_auto_reply(request.content, db)
    if auto_reply:
        reply_message = ChatMessage(
            session_id=session.id,
            sender_type="system",
            content=auto_reply,
            message_type="text"
        )
        db.add(reply_message)
        db.commit()
    
    return success_response(data={
        "message_id": user_message.id,
        "created_at": user_message.created_at.strftime("%Y-%m-%d %H:%M:%S") if user_message.created_at else None
    })


def get_auto_reply(content: str, db: Session) -> Optional[str]:
    """获取自动回复"""
    content_lower = content.lower()
    
    # 查找匹配的快捷回复
    quick_replies = db.query(QuickReply).filter(QuickReply.is_active == True).all()
    for qr in quick_replies:
        if qr.question.lower() in content_lower or content_lower in qr.question.lower():
            return qr.answer
    
    # 默认关键词回复
    keywords = {
        "价格": "我们的检测价格根据项目不同而有所差异，您可以在项目详情页查看具体价格，或者告诉我您需要检测的项目，我为您查询。",
        "多久": "一般检测周期为3-7个工作日，具体时间取决于检测项目的复杂程度。",
        "报告": "检测完成后，您可以在【我的订单】-【已完成】中下载电子版报告，纸质报告会邮寄到您预留的地址。",
        "样品": "您可以通过快递寄送样品到我们的实验室，具体地址会在下单后通过短信发送给您。",
        "发票": "我们支持增值税普通发票和专用发票，您可以在订单完成后申请开具发票。",
        "退款": "如果检测尚未开始，您可以申请全额退款；如果已开始检测，可能会产生部分费用，具体请联系人工客服处理。"
    }
    
    for keyword, reply in keywords.items():
        if keyword in content:
            return reply
    
    # 默认回复
    return "感谢您的咨询，人工客服正在为您接入，请稍候...如有紧急问题，您也可以拨打客服电话：17819781949"


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
        db.commit()
    
    return success_response(message="会话已关闭")
