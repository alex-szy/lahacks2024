from datetime import datetime
import reflex as rx

class message(rx.Model, table=True):
    # sender: str = Field(foreign_key= 'User.username')
    # recipient: str = Field(foreign_key= 'User.username')
    sender: str
    recipient: str
    convo_id: str
    content: str
    timestamp: datetime