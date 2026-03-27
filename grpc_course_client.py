import grpc
import course_service_pb2
import course_service_pb2_grpc


def run():
    """Connect to gRPC server and call GetCourse method"""
    # Create a channel to connect to the server
    channel = grpc.insecure_channel('localhost:50051')

    # Create a stub (client)
    stub = course_service_pb2_grpc.CourseServiceStub(channel)

    # Create a request
    request = course_service_pb2.GetCourseRequest(course_id="api-course")

    # Call the remote method
    response = stub.GetCourse(request)

    # Print the response
    print(response)

    # Close the channel
    channel.close()


if __name__ == "__main__":
    run()
