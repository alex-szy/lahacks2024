import reflex as rx
from lahacks2024 import styles
from lahacks2024.templates import template
from reflex_magic_link_auth import MagicLinkAuthState
from ..backend.user import User
from ..backend.message import Message
from datetime import datetime
    

class ChatRoomState(rx.State):
    curr_sender: User | None
    curr_recipient: User | None
    messages: list[Message] = []

    async def load_users(self):
        authstate = await self.get_state(MagicLinkAuthState)
        if not authstate.session_is_valid:
            return rx.redirect('/login')
        chat_id = self.router.page.params.get("chat_id")
        if chat_id is None:
            return rx.redirect('/')
        users = chat_id.split('+')
        with rx.session() as session:
            user = session.exec(
                User.select().where(
                    User.persistent_id == authstate.auth_session.persistent_id
                )
            ).first()
            if user is None:
                # user does not exist
                return rx.redirect('/')
            try:
                idx = users.index(user.persistent_id)
            except ValueError:
                return rx.redirect('/')
            recipient = session.exec(
                User.select().where(
                    User.persistent_id == users[1 - idx]
                )
            ).first()
            if recipient is None:
                # recipient does not exist
                return rx.redirect('/')
        self.curr_sender = user
        self.curr_recipient = recipient
        return self.retrieve_messages()
    

    async def retrieve_messages(self):
        with rx.session() as session:
            messages = session.exec(
                Message.select().where(
                    (Message.sender == self.curr_sender.persistent_id and Message.recipient == self.curr_recipient.persistent_id)
                    or (Message.sender == self.curr_recipient.persistent_id and Message.recipient == self.curr_sender.persistent_id)
                )
            ).all()

        self.messages = messages


    async def send_message(self, content: str):
        authstate = await self.get_state(MagicLinkAuthState)
        if not authstate.session_is_valid:
            return rx.redirect('/login')
        with rx.session() as session: #add message to table, want to update state of the table
            #when state of table is updated,
            session.add(
                Message(
                    sender = self.curr_sender.persistent_id,
                    recipient = self.curr_recipient.persistent_id,
                    content = content,
                    timestamp = datetime.now()
                )
            )
            session.commit()
        return rx.redirect('/chatroom')
    

class MessageFormState(rx.State):
    async def handle_submit(self, form_data):
        chatroom = await self.get_state(ChatRoomState)
        return chatroom.send_message(form_data.get('message'))


# Components

def message_bar() -> rx.Component:
    return rx.form.root(
        rx.flex(
            rx.form.field(
                rx.form.control(
                    rx.input.input(
                        placeholder="Send a message...",
                    ),
                    as_child=True,
                ),
                width="100%",
                margin_right="1em",
                name="message",
            ),
            rx.form.submit(
                rx.button("Send",style=styles.button_style),
                as_child=True,
            ),
            justify="between",
            align="stretch",
        ),
        reset_on_submit=True,
        on_submit=MessageFormState.handle_submit,
    )


def message_display() -> rx.Component:
    # conv_id = sorted(sender,recipient)
    # def get_users(self):
    return rx.flex(
        rx.foreach(ChatRoomState.messages, render),
        direction="column",
    )


def render(display: Message) -> rx.Component:
    # language = display.sender.language
    return rx.cond(
        display.sender == ChatRoomState.curr_sender.persistent_id,
        rx.flex(
            rx.box(rx.text(display.content, style=styles.question_style)),
            justify="end",
            width="100%"
        ),
        rx.flex(
            rx.box(rx.text(display.content, style=styles.answer_style)),
            justify="start",
            width="100%"
        ),
    )


@template(route="/chatroom/[chat_id]",title="Chatroom", on_load=ChatRoomState.load_users())
def chatroom() -> rx.Component:
    return rx.flex(
        message_display(),
        message_bar(),
        direction="column",
        width="100%",
    )