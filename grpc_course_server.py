import grpc
from concurrent import futures
import course_service_pb2
import course_service_pb2_grpc


class CourseServicer(course_service_pb2_grpc.CourseServiceServicer):
    """Implementation of CourseService"""

    def GetCourse(self, request, context):
        """
        Handle GetCourse RPC call

        Args:
            request: GetCourseRequest with course_id
            context: gRPC context

        Returns:
            GetCourseResponse with course information
        """
        return course_service_pb2.GetCourseResponse(
            course_id=request.course_id,
            title="Автотесты API",
            description="Будем изучать написание API автотестов"
        )


def serve():
    """Start the gRPC server on port 50051"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    course_service_pb2_grpc.add_CourseServiceServicer_to_server(
        CourseServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    print("Server starting on port 50051...")
    server.start()
    print("Server is running. Press Ctrl+C to stop.")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
