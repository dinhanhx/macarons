import random

from macarons.image_text import generate_datapoint


def test_generate_datapoint():
    random.seed(42)
    dp = generate_datapoint(256, 256)
    dp.make_caption()
    dp.make_question_answer_list()
    assert dp.circle_color_name == 'darkmagenta'
    assert dp.background_color_name == 'bisque'
    assert dp.caption == 'The darkmagenta circle on the bisque background'

    question_answer_list = [
        ["What is the color of the circle", "darkmagenta"],
        ["What is the color of the background", "bisque"],
        [
            "What are the color of the circle and the background",
            "darkmagenta and bisque",
        ],
    ]
    for i in range(len(question_answer_list)):
        for ii in range(2):
            assert question_answer_list[i][ii] == dp.question_answer_list[i][ii]
