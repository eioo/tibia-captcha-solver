import re
import time

import cv2
import numpy as np
import pyautogui
from PIL import Image
from pytesseract import pytesseract

lower_rgb = 150
upper_rgb = 255
debug = True


def filter_color(image):
    # It converts the BGR color space of image to HSV color space
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Threshold of blue in HSV space
    lower_blue = np.array([lower_rgb] * 3)
    upper_blue = np.array([upper_rgb] * 3)

    # preparing the mask to overlay
    mask = cv2.inRange(rgb, lower_blue, upper_blue)

    # The black region in the mask has the value of 0,
    # so when multiplied with original image removes all non-blue regions
    result = cv2.bitwise_and(image, image, mask=mask)
    result = cv2.bitwise_not(result)

    img = np.array(result)
    new_x, new_y = img.shape[1] * 2, img.shape[0] * 2
    resized_img = cv2.resize(img, (int(new_x), int(new_y)), interpolation=cv2.INTER_NEAREST)

    if debug:
        cv2.imwrite('cropped_inverse.png', resized_img)

    return resized_img


def crop_captcha(region):
    x = region.left - 51
    y = region.top + 60
    w = 375
    h = 100

    if debug:
        cropped_img = pyautogui.screenshot('cropped.png', region=(x, y, w, h))
    else:
        cropped_img = pyautogui.screenshot(region=(x, y, w, h))

    return {
        'img': np.array(cropped_img),
        'x': x,
        'y': y
    }


def locate_captcha():
    return pyautogui.locateOnScreen('captcha_corner.png', confidence=0.9)


def replace_all(text, replacements):
    for r in replacements:
        text = text.replace(r[0], r[1])
    return text


def solve_captcha(image):
    #  --psm 6    Assume a single uniform block of text.
    image = Image.fromarray(image)
    text = pytesseract.image_to_string(image, config=f'--psm 6')
    text = replace_all(text, [['G', '6'], ['o', '0'], ['O', '0'], ['s', '5'], ['S', '5']])

    try:
        expr = replace_all(text.split('\n')[0], [[' ', ''], ['.', ''], [',', '']])

        if not expr:
            print(text)
            return False

    except:
        print(text)
        return False

    answer = eval(expr)
    choices = [int(n) for n in re.findall(r'\n+(-?\d+)', text)]
    print(f'{expr} = {answer}')

    try:
        return choices.index(answer)
    except ValueError:
        return False


def click_choice(x, y, index):
    choice_x = x + 10
    choice_y = y + 25 + index * 14
    print(f'Selecting choice #{index + 1} ({choice_x}, {choice_y})')
    pyautogui.click(choice_x, choice_y)


def click_select(x, y):
    pyautogui.click(x + 286, y + 115)


def main():
    print('Waiting for captcha')

    while True:
        captcha_region = locate_captcha()

        if captcha_region:
            break

        time.sleep(2)

    print('Captcha found')

    cropped = crop_captcha(captcha_region)
    filtered = filter_color(cropped['img'])

    choice_index = solve_captcha(filtered)

    if choice_index is False:
        print('Failed to solve')
        return

    click_choice(cropped['x'], cropped['y'], choice_index)
    time.sleep(1)
    click_select(cropped['x'], cropped['y'])
    time.sleep(1)
    pyautogui.typewrite('!me')
    print('Done')

    main()


main()
