import random
import os
import config2
import imageio.v2 as imageio
from visualizer2 import drawBelG
from visualizer2 import drawG
from visualizer2 import drawGrT
from agent2 import runagent
from grid_gen2 import gengrid
import shutil
from grid_gen2 import belief_grid
from grid_gen2 import scan_infor

def printgrid(grid):
    print("\n --- Initial Grid ---")
    for a in range(config2.M):
        row=""
        for b in range(config2.N):
            row+=f"{grid[a][b]}"
        print(row)
        
def savegif(frame_d, output):
    images=[]
    files = sorted(os.listdir(frame_d),key=lambda x: int(x.split('_')[1].split('.')[0]))
    for file in files:
        images.append(imageio.imread(os.path.join(frame_d, file)))
    imageio.mimsave(output, images, fps=config2.FPS)
    
def main():
    random.seed(config2.RANDOM_SEED)
    grid, gpath, anchor1, anchor2=gengrid()
    print("Anchor 1: ", anchor1)
    print("Anchor 2: ", anchor2)
    printgrid(grid)
    belfG=belief_grid(config2.M, config2.N)
    scan_I=scan_infor(config2.M, config2.N)
    drawG(grid=grid, belief_g=belfG, scan_info=scan_I, agent_pos=None, turns=0, time=0, lives=config2.INITIAL_LIVES, path=None, save_path=None)
    executed_path=runagent(grid, belfG, scan_I)
    print("\n PATH ")
    for step in executed_path:
        print(step)
        
    
    
    if os.path.exists(config2.FRAME_SAVE_DIR):
        shutil.rmtree(config2.FRAME_SAVE_DIR)

    os.makedirs(config2.FRAME_SAVE_DIR)
    total_time = 0
    total_turns = 0
    for i in range(len(executed_path)):
        r, c, action, lives=executed_path[i]
        if i > 0:
            if action == 'walk':
                total_time += config2.WALK_TIME_COST
            elif action == 'jump':
                total_time += config2.JUMP_TIME_COST
            if action == 'scan':
                total_turns+=config2.SCAN_TURN_COST

            total_turns += config2.TURN_COST

        partial_path = executed_path[:i+1]
        drawG(
            grid,
            belfG, 
            scan_I, 
            agent_pos=(r, c),
            path=partial_path,
            lives=lives,
            time=total_time,
            turns=total_turns,
            save_path=f"{config2.FRAME_SAVE_DIR}/frame2_{i}.png"
        )
        savegif(config2.FRAME_SAVE_DIR, config2.GIF_NAME)

        print("\nSimulation saved as:", config2.GIF_NAME)
        
if __name__ == "__main__":
    main()
            