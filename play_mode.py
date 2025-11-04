import random
from pico2d import *

import game_framework
import game_world

from boy import Boy
from grass import Grass
from ball import Ball
from zombie import Zombie

boy = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global boy
    global balls

    grass = Grass()
    game_world.add_object(grass, 0)
    game_world.add_collision_pair('grass:ball', grass, None) #[[grass], []]

    boy = Boy()
    game_world.add_object(boy, 1)

    balls = [Ball(random.randint(100, 1600-100),60,0)for _ in range(30)]
    game_world.add_objects(balls, 1)

    zombies = [Zombie() for _ in range(4)]
    game_world.add_objects(zombies,1)

    #소년과 공 사이에 충돌검사가 필요하다는 정보를 추가
    game_world.add_collision_pair('boy:ball', boy, None) #[[boy], []]
    for ball in balls:
        game_world.add_collision_pair('boy:ball',None,ball)#[[boy], [ball1, ball2, ...]]
    #좀비랑 공 사이 + 소년과 좀비의 충돌검사
    for zombie in zombies:
        game_world.add_collision_pair('boy:zombies',None,zombie)
        game_world.add_collision_pair('zombies:ball', zombie, None)

def update():
    game_world.update()
    #충돌 처리할 객체들이 적으면 상관 없지만 많다면? => 충돌그룹을 만들어서 처리 ex) boy:ball, grass:ball
    #for ball in balls.copy():
        #if game_world.collide(boy, ball):
         #   print('COLLISION boy: ball')
         #   boy.ball_count += 1
         #   game_world.remove_object(ball)
            #게임월드에서는 지워졌지만 balls 리스트에서는 남아있으므로 제거
         #   balls.remove(ball)
    game_world.handle_collisions()



def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

