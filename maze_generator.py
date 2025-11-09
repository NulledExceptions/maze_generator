
import argparse, os, matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke
from utils.config import OUTPUT_DIR, LOG_DIR, DIFFICULTY_SETTINGS
from utils.logger_setup import setup_logger
from maze_shapes.rectangular_maze import RectangularMaze
from pdf_generator import MazePDFGenerator

def outline_text(ax, text, pos):
    ax.text(*pos, text, color='black', fontsize=10, weight='bold',
            path_effects=[withStroke(linewidth=3, foreground='white')],
            ha='center', va='center')

def label_position(cell, h, w, pad=1.0):
    x, y = cell
    lx, ly = y + 0.5, h - x - 0.5
    if x == 0:           # top edge -> above
        ly += pad
    elif x == h - 1:     # bottom edge -> below
        ly -= pad
    elif y == 0:         # left edge -> left
        lx -= pad
    elif y == w - 1:     # right edge -> right
        lx += pad
    return lx, ly

def draw_rectangular(maze, start, end, path=None, name='maze.png', wall_thickness=2):
    h, w = maze.shape
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_aspect('equal'); ax.set_facecolor('white')

    # Draw continuous walls: edges between wall(1) and passage(0) or boundary
    for i in range(h):
        for j in range(w):
            if maze[i,j] == 0: 
                continue
            if i==0 or maze[i-1,j]==0: ax.plot([j,j+1],[h-i,h-i],'k',lw=wall_thickness)
            if i==h-1 or maze[i+1,j]==0: ax.plot([j,j+1],[h-i-1,h-i-1],'k',lw=wall_thickness)
            if j==0 or maze[i,j-1]==0: ax.plot([j,j],[h-i-1,h-i],'k',lw=wall_thickness)
            if j==w-1 or maze[i,j+1]==0: ax.plot([j+1,j+1],[h-i-1,h-i],'k',lw=wall_thickness)

    # Draw solution (black dashed, to keep B/W)
    if path:
        px=[y+0.5 for (x,y) in path]
        py=[h-x-0.5 for (x,y) in path]
        ax.plot(px,py,'--',color='black',lw=1.4)

    # Markers
    sx,sy=start[1]+0.5,h-start[0]-0.5
    ex,ey=end[1]+0.5,h-end[0]-0.5
    ax.scatter([sx],[sy],c='white',s=60,edgecolors='black',zorder=5)
    ax.scatter([ex],[ey],c='white',s=60,edgecolors='black',zorder=5)

    # Labels OUTSIDE with padding, horizontal
    slx, sly = label_position(start, h, w, pad=1.0)
    elx, ely = label_position(end, h, w, pad=1.0)
    outline_text(ax,'Start',(slx, sly))
    outline_text(ax,'End',(elx, ely))

    ax.axis('off'); plt.xlim(0,w); plt.ylim(0,h)
    fig.savefig(name,dpi=300,bbox_inches='tight',pad_inches=0); plt.close(fig)
    return name

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',choices=list(DIFFICULTY_SETTINGS.keys()),default='medium')
    parser.add_argument('--wall_thickness',type=float,default=2.0)
    args=parser.parse_args()

    logger,_=setup_logger(LOG_DIR)
    settings=DIFFICULTY_SETTINGS[args.difficulty]
    pdf=MazePDFGenerator(OUTPUT_DIR,logger)
    gen=RectangularMaze(settings['grid_size'],logger)
    maze,start,end,path=gen.generate()
    maze_img=draw_rectangular(maze,start,end,name='maze.png',wall_thickness=args.wall_thickness)
    sol_img=draw_rectangular(maze,start,end,path,name='solution.png',wall_thickness=args.wall_thickness)
    pdf.save_pdf(maze_img,sol_img)
    print('Maze generation complete!')

if __name__=='__main__': 
    main()
