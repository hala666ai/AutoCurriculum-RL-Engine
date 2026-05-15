import random
import numpy as np

class StudentEnv:
    def __init__(self):
        # skills: accuracy probability for each domain
        self.skills = {"algebra":0.5,"geometry":0.4,"probability":0.3,"sequences":0.35}
    def step(self, exercise):
        acc = self.skills[exercise]
        success = random.random() < acc
        reward = 1 if success else -1
        # update skill level
        if success:
            self.skills[exercise] = min(1.0, acc + 0.05)
        else:
            self.skills[exercise] = max(0.0, acc - 0.02)
        return reward, success

class RLAgent:
    def __init__(self, exercises):
        self.q = {e:0.0 for e in exercises}
        self.alpha = 0.1
        self.gamma = 0.9
    def choose(self):
        if random.random() > 0.2: # epsilon-greedy
            return max(self.q, key=self.q.get)
        return random.choice(list(self.q.keys()))
    def update(self, exercise, reward):
        old = self.q[exercise]
        self.q[exercise] = old + self.alpha*(reward + self.gamma*old - old)

def run_simulation():
    env = StudentEnv()
    agent = RLAgent(["algebra","geometry","probability","sequences"])
    for step in range(30):
        ex = agent.choose()
        reward, success = env.step(ex)
        agent.update(ex, reward)
        print(f"Step {step+1}: {ex} | Success={success} | Reward={reward} | Skill={env.skills[ex]:.2f}")

if __name__ == "__main__":
    run_simulation()