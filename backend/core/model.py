from pgvector.sqlalchemy import Vector
from sqlmodel import Field, Relationship, SQLModel, LargeBinary
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, Text, DateTime, func


class Roles(SQLModel, table=True):
    __tablename__ = "roles"
    role_id: int | None = Field(default=None, primary_key=True)
    role: str = Field(default="user")
    webuser: List["WebUsers"] = Relationship(back_populates="role")


class WebUsers(SQLModel, table=True):
    __tablename__="web_users"
    web_user_id: int | None = Field(default=None, primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="roles.role_id")
    username: Optional[str] = Field(default=None, sa_column=Column(Text))
    email: Optional[str] = Field(default=None, sa_column=Column(Text))
    password: Optional[str] = Field(default=None, sa_column=Column(Text))
    image: Optional[str] = Field(default=None, sa_column=Column(Text))
    email_verified: Optional[bool] = False
    create_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    update_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now())) 
    role: Optional[Roles] = Relationship(back_populates="webuser")
    emailverificationtoken: List["EmailVerificationTokens"] = Relationship(back_populates="webuser", sa_relationship_kwargs={"passive_deletes": True})
    updatepasswordtoken: List["UpdatePasswordTokens"] = Relationship(back_populates="webuser", sa_relationship_kwargs={"passive_deletes": True})
    account: List["Accounts"] = Relationship(back_populates="webuser", sa_relationship_kwargs={"passive_deletes": True})
    ragfiles: List["RagFiles"] = Relationship(back_populates="webuser", sa_relationship_kwargs={"passive_deletes": True})
    webchats: List["WebChats"] = Relationship(back_populates="webuser", sa_relationship_kwargs={"passive_deletes": True})


class EmailVerificationTokens(SQLModel, table=True):
    __tablename__="email_verification_tokens"
    email_verification_token_id: int | None = Field(default=None, primary_key=True)
    web_user_id: Optional[int] = Field(default=None, foreign_key="web_users.web_user_id", ondelete="CASCADE")
    email_verification_token: Optional[str] = Field(default=None, sa_column=Column(Text))
    create_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    update_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    expires_at: Optional[datetime] = None
    webuser: Optional[WebUsers] = Relationship(back_populates="emailverificationtoken", sa_relationship_kwargs={"passive_deletes": True})


class UpdatePasswordTokens(SQLModel, table=True):
    __tablename__="update_password_tokens" 
    update_password_token_id: int | None = Field(default=None, primary_key=True)
    web_user_id: Optional[int] = Field(default=None, foreign_key="web_users.web_user_id", ondelete="CASCADE")
    update_password_token: Optional[str] = Field(default=None, sa_column=Column(Text))
    create_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    update_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    expires_at: Optional[datetime] = None
    webuser: Optional[WebUsers] = Relationship(back_populates="updatepasswordtoken", sa_relationship_kwargs={"passive_deletes": True})


class Accounts(SQLModel, table = True):
    __tablename__ = "accounts"
    account_id: int | None = Field(default=None, primary_key=True)
    web_user_id: Optional[int] = Field(default=None, foreign_key="web_users.web_user_id", ondelete="CASCADE")
    account_type: Optional[str] = Field(default=None, sa_column=Column(Text))
    provider: Optional[str] = Field(default=None, sa_column=Column(Text))
    provider_account_id: Optional[str] = Field(default=None, sa_column=Column(Text))
    refresh_token: Optional[str] = Field(default=None, sa_column=Column(Text))
    access_token: Optional[str] = Field(default=None, sa_column=Column(Text))
    expires_at: Optional[datetime] = None
    token_type: Optional[str] = Field(default=None, sa_column=Column(Text))
    scope: Optional[str] = Field(default=None, sa_column=Column(Text))
    id_token: Optional[str] = Field(default=None, sa_column=Column(Text))
    session_state: Optional[str] = Field(default=None, sa_column=Column(Text))
    webuser: Optional[WebUsers] = Relationship(back_populates="account", sa_relationship_kwargs={"passive_deletes": True})


class RagFiles(SQLModel, table = True):
    __tablename__ = "rag_files"
    rag_file_id: int | None = Field(default=None, primary_key=True)
    web_user_id: Optional[int] = Field(default=None, foreign_key="web_users.web_user_id", ondelete="CASCADE")
    name: Optional[str] = Field(default=None, sa_column=Column(Text))
    detail: Optional[str] = Field(default=None, sa_column=Column(Text))
    type: Optional[str] = Field(default=None, sa_column=Column(Text))
    chunk: Optional[str] = Field(default=None, sa_column=Column(Text))
    file_path: Optional[str] = Field(default=None, sa_column=Column(Text))
    create_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    update_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    webuser: Optional[WebUsers] = Relationship(back_populates="ragfiles", sa_relationship_kwargs={"passive_deletes": True})


class WebChats(SQLModel, table = True):
    __tablename__ = "web_chats"
    web_chat_id: int | None = Field(default=None, primary_key=True)
    web_user_id: Optional[int] = Field(default=None, foreign_key="web_users.web_user_id", ondelete="CASCADE")
    chat_name: Optional[str] = Field(default=None, sa_column=Column(Text))
    create_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    update_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    webmessage: List["WebMessages"] = Relationship(back_populates="webchat", sa_relationship_kwargs={"passive_deletes": True})
    webuser: Optional[WebUsers] = Relationship(back_populates="webchats", sa_relationship_kwargs={"passive_deletes": True})


class WebMessages(SQLModel, table = True):
    __tablename__ = "web_messages"
    web_message_id: int | None = Field(default=None, primary_key=True)
    web_chat_id: Optional[int] = Field(default=None, foreign_key="web_chats.web_chat_id", ondelete="CASCADE")
    query_message: Optional[str] = Field(default=None, sa_column=Column(Text))
    response_message: Optional[str] = Field(default=None, sa_column=Column(Text))
    rating: Optional[int] = None
    create_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    update_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    webchat: Optional[WebChats] = Relationship(back_populates="webmessage", sa_relationship_kwargs={"passive_deletes": True})


class LineUsers(SQLModel, table=True):
    __tablename__="line_users"
    line_user_id: int | None = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, sa_column=Column(Text))
    create_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    linemessage: List["LineMessages"] = Relationship(back_populates="lineuser", sa_relationship_kwargs={"passive_deletes": True})


class LineMessages(SQLModel, table = True):
    __tablename__ = "line_messages"
    line_message_id: int | None = Field(default=None, primary_key=True)
    line_user_id: Optional[int] = Field(default=None, foreign_key="line_users.line_user_id", ondelete="CASCADE")
    query_message: Optional[str] = Field(default=None, sa_column=Column(Text))
    response_message: Optional[str] = Field(default=None, sa_column=Column(Text))
    create_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    update_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    lineuser: Optional[LineUsers] = Relationship(back_populates="linemessage", sa_relationship_kwargs={"passive_deletes": True})