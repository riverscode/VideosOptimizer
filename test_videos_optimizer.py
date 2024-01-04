import os
import pytest
from videos_optimizer import get_paths, get_files, optimize_video, generate_pdf_report, process_videos

# Define a fixture for test data
@pytest.fixture
def test_data_folder(tmpdir):
    # Create a temporary folder for testing
    folder = tmpdir.mkdir("test_data")
    return folder

# Test get_paths function
def test_get_paths(test_data_folder):
    input_folder, output_folder, pdf_report = get_paths(str(test_data_folder))
    assert os.path.exists(input_folder)
    assert os.path.exists(output_folder)
    assert pdf_report.endswith('optimized_videos_report.pdf')

# Test get_files function
def test_get_files(test_data_folder):
    # Create some dummy video files in the test folder
    test_data_folder.join("first_video.mp4").write("")
    test_data_folder.join("second_video.avi").write("")
    test_data_folder.join("document.pdf").write("")

    input_files = get_files(str(test_data_folder))
    assert "first_video.mp4" in input_files
    assert "second_video.avi" in input_files
    assert "document.pdf" not in input_files


# Test generate_pdf_report function
def test_generate_pdf_report(test_data_folder):
    pdf_path = str(test_data_folder.join("test_report.pdf"))
    video_info = [["first_video.mp4", 100, 50, "78.00%"], ["second_video.avi", 200, 100, "90.00%"]]

    generate_pdf_report(pdf_path, video_info, str(test_data_folder))

    assert os.path.exists(pdf_path)

# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])