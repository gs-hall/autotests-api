from google.protobuf.message import Message

class GetCourseRequest(Message):
    course_id: str
    def __init__(self, *, course_id: str = ...) -> None: ...

class GetCourseResponse(Message):
    course_id: str
    title: str
    description: str
    def __init__(
        self,
        *,
        course_id: str = ...,
        title: str = ...,
        description: str = ...,
    ) -> None: ...
