from config import HAZ_TYPES
import random
import os
import config
import imageio.v2 as imageio
from visualizer import drawG
from agent import search
from grid_gen import gengrid
import shutil
import config

def printgrid(grid):
    print("\n --- Initial Grid ---")
    for a in range(config.M):
        row=""
        for b in range(config.N):
            row+=f"{grid[a][b]}"
        print(row)
        
def savegif(frame_d, output):
    images=[]
    files = sorted(os.listdir(frame_d),key=lambda x: int(x.split('_')[1].split('.')[0]))
    for file in files:
        images.append(imageio.imread(os.path.join(frame_d, file)))
    imageio.mimsave(output, images, fps=config.FPS)
    
def main():
    random.seed(config.RANDOM_SEED)
    grid, gpath, anchor1, anchor2=gengrid()
    print("Anchor 1: ", anchor1)
    print("Anchor 2: ", anchor2)
    printgrid(grid)
    drawG(grid=grid, agent_pos=None, turns=0, time=0, lives=config.INITIAL_LIVES, path=gpath, save_path=None)
    optimal_path = search(grid)

    if optimal_path is None:
        print("No path found.")
        return

    print("\n=== OPTIMAL PATH ===")
    for step in optimal_path:
        print(step)
        
    
    
    if os.path.exists(config.FRAME_SAVE_DIR):
        shutil.rmtree(config.FRAME_SAVE_DIR)

    os.makedirs(config.FRAME_SAVE_DIR)
    total_time = 0
    total_turns = 0
    for i in range(len(optimal_path)):
        r, c, action, lives=optimal_path[i]
        if i > 0:
            if action == 'walk':
                total_time += config.WALK_TIME_COST
            elif action == 'jump':
                total_time += config.JUMP_TIME_COST

            total_turns += config.TURN_COST

        partial_path = optimal_path[:i+1]
        drawG(
            grid,
            agent_pos=(r, c),
            path=partial_path,
            lives=lives,
            time=total_time,
            turns=total_turns,
            save_path=f"{config.FRAME_SAVE_DIR}/frame_{i}.png"
        )
        savegif(config.FRAME_SAVE_DIR, config.GIF_NAME)

        print("\nSimulation saved as:", config.GIF_NAME)
        
if __name__ == "__main__":
    main()
            
