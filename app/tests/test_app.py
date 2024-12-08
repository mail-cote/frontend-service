import unittest
from unittest.mock import MagicMock, patch
import app
import member_pb2

class TestAppService(unittest.TestCase):

    @patch('app.get_grpc_stub')
    def test_get_member_id(self, mock_get_grpc_stub):
        # Mock gRPC Stub 및 응답 설정
        mock_stub = MagicMock()
        mock_stub.GetMemberByEmail.return_value = member_pb2.GetMemberByEmailResponse(member_id=123)
        mock_get_grpc_stub.return_value = mock_stub

        # 테스트
        result = app.get_member_id("test@example.com")
        self.assertEqual(result, 123)
        mock_stub.GetMemberByEmail.assert_called_once_with(
            member_pb2.GetMemberByEmailRequest(email="test@example.com")
        )


    @patch('app.get_grpc_stub')
    @patch('app.get_member_id')
    def test_update_member(self, mock_get_member_id, mock_get_grpc_stub):
        # Mock gRPC Stub 및 응답 설정
        mock_stub = MagicMock()
        mock_stub.UpdateMember.return_value = member_pb2.UpdateMemberResponse(message="Member updated successfully!")
        mock_get_grpc_stub.return_value = mock_stub
        mock_get_member_id.return_value = 123

        email = "test@example.com"
        old_password = "old_password"
        new_level = "Silver3"
        new_password = "new_password"

        # 테스트
        response = app.update_member(email, old_password, new_level, new_password)
        self.assertEqual(response, "Member updated successfully!")
        mock_stub.UpdateMember.assert_called_once_with(
            member_pb2.UpdateMemberRequest(
                member_id=123,
                level=new_level,
                password=new_password,
                old_password=old_password
            )
        )


if __name__ == "__main__":
    unittest.main()
