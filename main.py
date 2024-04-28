import streamlit as st
import gym
import numpy as np
import cv2


def initialize_frame():
    width, height = 600, 200
    img = np.ones(shape=(height, width, 3)) * 255.0
    margin_horizontal = 6
    margin_vertical = 2

    for i in range(13):
        img = cv2.line(img, (49 * i + margin_horizontal, margin_vertical),
                       (49 * i + margin_horizontal, 200 - margin_vertical), color=(0, 0, 0), thickness=1)

    for i in range(5):
        img = cv2.line(img, (margin_horizontal, 49 * i + margin_vertical),
                       (600 - margin_horizontal, 49 * i + margin_vertical), color=(0, 0, 0), thickness=1)

    img = cv2.rectangle(img, (49 * 1 + margin_horizontal + 2, 49 * 3 + margin_vertical + 2),
                        (49 * 11 + margin_horizontal - 2, 49 * 4 + margin_vertical - 2), color=(255, 0, 255),
                        thickness=-1)
    img = cv2.putText(img, text="Cliff", org=(49 * 5 + margin_horizontal, 49 * 4 + margin_vertical - 10),
                      fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

    frame = cv2.putText(img, text="G", org=(49 * 11 + margin_horizontal + 10, 49 * 4 + margin_vertical - 10),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0), thickness=2)
    return frame


def put_agent(img, state):
    margin_horizontal = 6
    margin_vertical = 2
    if isinstance(state, tuple):
        state_value = state[0]
    else:
        state_value = state
    row = state_value // 12
    column = state_value % 12

    img_with_agent = img.copy()
    cv2.putText(img_with_agent, text="A", org=(49 * column + margin_horizontal + 10, 49 * (row + 1) + margin_vertical - 10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0), thickness=2)
    
    # Normalize image data
    img_with_agent_normalized = img_with_agent / 255.0
    
    return img_with_agent_normalized

def action_to_direction(action):
    if action == 0:
        return "Up"
    elif action == 1:
        return "Right"
    elif action == 2:
        return "Down"
    elif action == 3:
        return "Left"
    else:
        return "Invalid"

def display_transition():
    done = False
    frame = initialize_frame()
    initial_state = cliffEnv.reset()
    while not done:
        frame = put_agent(frame.copy(), initial_state)  # Always show the agent at the initial state
        cv2.imshow("Cliff World", frame)
        action = cliffEnv.action_space.sample()
        st.write("Now the agent took ->>>>", action_to_direction(action))  # Print the direction
        step_result = cliffEnv.step(action)
        next_state, reward, done, info, *_ = step_result
        if next_state == initial_state:  # If the agent returns to the initial state, reset the frame
            frame = initialize_frame()
        initial_state = next_state

    cliffEnv.close()


cliffEnv = gym.make('CliffWalking-v0')

# Streamlit app
st.title("Cliff Walking Environment")
display_transition()
