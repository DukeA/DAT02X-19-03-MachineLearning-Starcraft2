from collections import deque
import random


class StateActionBuffer(object):
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.buffer = deque()
        self.buffer_length = 0

    def add(self, state, action, new_state, reward):
        data = (state[0], action, new_state[0], reward, False)
        if self.buffer_length < self.buffer_size:
            self.buffer.append(data)
            self.buffer_length += 1
        else:
            self.buffer.popleft()
            self.buffer.append(data)

    def get_buffer(self):
        return list(self.buffer)

    def get_batch(self, batch_size):
        if self.buffer_length < batch_size:
            return random.sample(self.buffer, self.buffer_length)
        else:
            return random.sample(self.buffer, batch_size)

    def get_newest_data(self):
        return self.buffer[len(self.buffer)-1]

    def set_newest_data(self, data_new):
        if len(data_new) == self.buffer_size:
            self.buffer.pop()
            self.buffer.append(data_new)
        else:
            print("Error when setting new buffer data.")

    def set_latest_done(self):
        data = self.get_newest_data()
        data_new = (data[0], data[1], data[2], data[3], True)
        self.buffer.pop()
        self.buffer.append(data_new)

    def set_latest_reward(self, reward):
        data = self.get_newest_data()
        data_new = (data[0], data[1], data[2], reward, data[4])
        self.buffer.pop()
        self.buffer.append(data_new)

    def reset(self):
        self.buffer = deque()
