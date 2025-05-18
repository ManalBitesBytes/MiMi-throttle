from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ai_services.file_2_text.file2text_utils.file2text_constant import MAX_FILE_SIZE
from ai_services.file_2_text.file_to_text_v1 import File2TextConverter


#######################################################################################################################
@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])  # AllowAny
def File2TextConverterAPI(request):
    user_id = request.user.id

    # Get Request/File Identifier as input.
    data = request.data
    request_id = None
    try:
        request_id = str(data['request_id'])
        if not request_id:
            return Response({"status_code": 1, "message": "Empty 'request_id'!"},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status_code": 2, "message": "Invalid Request, it should include 'request_id'! "},
                        status=status.HTTP_400_BAD_REQUEST)

    file_obj = request.FILES.get("file")  # equest.FILES.getlist("candidate_resumes[]")
    if not file_obj:
        return Response(
            {"status_code": 3, "message": "Empty file!!!"},
            status=status.HTTP_400_BAD_REQUEST)

    if file_obj.size > MAX_FILE_SIZE:  # file size  check
        return Response(
            {"status_code": 6, "message": "The max file size is " + str(MAX_FILE_SIZE)},
            status=status.HTTP_400_BAD_REQUEST)

    file_type, file_content, file_languages = File2TextConverter().convert_file_to_text(request_id, file_obj)
    if file_type == -1:  # file type Not supported
        return Response({"status_code": 7,
                         "message": f"File type not supported!"},
                        status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"file_text": file_content, "file_type": file_type, "file_languages": file_languages})
