import random,sys,time
import pygame,pprint
from pygame.locals import *
#from settings import *

#color
white=(255,255,255)
black=(0,0,0)
gray1=(200,200,200)
gray2=(100,100,100)
blue=(0,0,255)
deepskyblue=(0,191,255)
green=(0,255,0)
red=(255,0,0)
#settings
boxsize=20
gapsize=2
state_height=30
game_boundary=10
option_height=15
level=9
mines_number=10
#fps
fps=30

#context
flag_cnt=mines_number
chose_color={1:blue,2:green,3:red}
mines_map=[]
prefix_sum=[]
clicked=[]
box_mines=[]
rclicked=[]
def main():
	global level
	global mines_number
	global flag_cnt
	global mines_map
	global prefix_sum
	global clicked
	global box_mines
	global rclicked
	global game_flag#0 normal;1 win;2 failure
	option_flag=0
	time=0
	game_flag=0
	time_start=False
	WINDOWWIDTH=level*(boxsize+2*gapsize)+game_boundary*2
	WINDOWHEIGHT=level*(boxsize+2*gapsize)+game_boundary+game_boundary*2+state_height+option_height
	running=True
	
	pygame.init()
	FPSCLOCK=pygame.time.Clock()
	Font=pygame.font.SysFont('bauhaus93',boxsize-2,bold=True)
	
	WINDOW=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))

	mousex=0
	mousey=0
	pygame.display.set_caption("Minesweeper")

	creat_mines(mines_map,prefix_sum,clicked,box_mines,rclicked,level,mines_number)


	WINDOW.fill(gray1)

	while True:
		
		mouse_lclicked=False
		mouse_rclicked=False
		if(time_start):
			time+=1/30


		darw_map(level,WINDOW,WINDOWWIDTH,Font,flag_cnt,time,mousex,mousey,option_flag)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex,mousey=event.pos
			elif event.type == MOUSEBUTTONUP:
				
				mousex,mousey=event.pos
				if event.button == 1:
					mouse_lclicked=True
				elif event.button ==3:
					mouse_rclicked=True
		if(running):
			if(mouse_lclicked):
				#sweep

				box_X,box_Y=get_box(mousex,mousey,level)
				if(box_X!=None and box_Y!=None):
					time_start=True
					running=box_flip(box_X,box_Y,box_mines,WINDOW,Font,level)
					if not running:
						time_start=False
			if(mouse_rclicked):
				box_X,box_Y=get_box(mousex,mousey,level)
				if(box_X!=None and box_Y!=None):
					if(not clicked[box_X+1][box_Y+1] and flag_cnt>0):
						x,y=get_xy(box_X,box_Y)
						pygame.draw.ellipse(WINDOW,red,(x,y,boxsize,boxsize),width=1)
						clicked[box_X+1][box_Y+1]=1
						rclicked[box_X+1][box_Y+1]=1
						flag_cnt-=1
					elif(rclicked[box_X+1][box_Y+1]):
						clicked[box_X+1][box_Y+1]=0
						rclicked[box_X+1][box_Y+1]=0
						flag_cnt+=1
			if check_win():
				time_start=False
		#restart
		if(mouse_lclicked):
			#check state
			rect_state=pygame.Rect(game_boundary,game_boundary+option_height,WINDOWWIDTH-game_boundary*2,state_height)
			rect3=pygame.Rect(rect_state.centerx-(boxsize+4)//2,rect_state.top+3,boxsize+4,boxsize+4)
			if rect3.collidepoint(mousex,mousey):

				game_flag=0
				time_start=False
				running=True
				time=0
				reinit(level,mines_number)
			

			rect_option=pygame.Rect(2,0,30,option_height)
			if option_flag==0 and rect_option.collidepoint(mousex,mousey):
				option_flag=1
			elif option_flag==1:
				rect_junior=pygame.Rect((2+30+2)*0+2,0,30,option_height)
				rect_mid=pygame.Rect((2+30+2)*1+2,0,30,option_height)
				rect_senior=pygame.Rect((2+30+2)*2+2,0,30,option_height)
				rect_back=pygame.Rect((2+30+2)*3+2,0,30,option_height)
				if rect_junior.collidepoint(mousex,mousey):
					level=9
					mines_number=10
					flag_cnt=mines_number
					game_flag=0
					time_start=False
					running=True
					time=0
					reinit(level,mines_number)
					WINDOWWIDTH=level*(boxsize+2*gapsize)+game_boundary*2
					WINDOWHEIGHT=level*(boxsize+2*gapsize)+game_boundary+game_boundary*2+state_height+option_height
					WINDOW=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
					WINDOW.fill(gray1)
				if rect_senior.collidepoint(mousex,mousey):
					level=22
					mines_number=99
					flag_cnt=mines_number
					game_flag=0
					time_start=False
					running=True
					time=0
					reinit(level,mines_number)
					WINDOWWIDTH=level*(boxsize+2*gapsize)+game_boundary*2
					WINDOWHEIGHT=level*(boxsize+2*gapsize)+game_boundary+game_boundary*2+state_height+option_height
					WINDOW=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
					WINDOW.fill(gray1)
				if rect_mid.collidepoint(mousex,mousey):
					level=16
					mines_number=40
					flag_cnt=mines_number
					game_flag=0
					time_start=False
					running=True
					time=0
					reinit(level,mines_number)
					WINDOWWIDTH=level*(boxsize+2*gapsize)+game_boundary*2
					WINDOWHEIGHT=level*(boxsize+2*gapsize)+game_boundary+game_boundary*2+state_height+option_height
					WINDOW=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
					WINDOW.fill(gray1)
				if rect_back.collidepoint(mousex,mousey):
					option_flag=0


		pygame.display.update()
		FPSCLOCK.tick(fps)

def reinit(level,mines_number):

	global mines_map
	global prefix_sum
	global clicked
	global box_mines
	global rclicked

	mines_map=[]
	prefix_sum=[]
	clicked=[]
	box_mines=[]
	rclicked=[]
	creat_mines(mines_map,prefix_sum,clicked,box_mines,rclicked,level,mines_number)

def check_win():
	global game_flag
	
	if rclicked==mines_map and \
	(sum(sum(row) for row in clicked)-sum(sum(row) for row in rclicked))\
	==\
	level*level-mines_number:
		game_flag=1
		#print("you win!!!")
		return True
		#other things
	return False

def get_xy(box_X,box_Y):
	return (game_boundary+gapsize+box_X*(boxsize+2*gapsize),
		game_boundary*2+state_height+option_height+gapsize+box_Y*(boxsize+2*gapsize))

def draw_state(rect_state,WINDOW,Font,flag_cnt,time):

	rect1=pygame.Rect(rect_state.left+5,rect_state.top+5,boxsize*2,boxsize)
	pygame.draw.rect(WINDOW,black,rect1)
	text_surface1=Font.render(str(flag_cnt),False,red)
	WINDOW.blit(text_surface1,rect1)

	rect3=pygame.Rect(rect_state.centerx-(boxsize+4)//2,rect_state.top+3,boxsize+4,boxsize+4)
	pygame.draw.polygon(WINDOW,white,[(rect3.x,rect3.y),
		(rect3.x+rect3.width,rect3.y),
		(rect3.x,rect3.y+rect3.height)])
	pygame.draw.polygon(WINDOW,gray2,[(rect3.x+rect3.width,rect3.y+rect3.height),
		(rect3.x+rect3.width,rect3.y),
		(rect3.x,rect3.y+rect3.height)])
	pygame.draw.rect(WINDOW,gray1,
		(rect3.x+1,rect3.y+1,rect3.width-2,rect3.height-2))
	if game_flag==0:
		pygame.draw.ellipse(WINDOW,black,rect3,2)
	elif game_flag==2:
		pygame.draw.line(WINDOW,red,(rect3.x+5,rect3.y+5),(rect3.x+rect3.width-5,rect3.y+rect3.height-5),2)
		pygame.draw.line(WINDOW,red,(rect3.x+rect3.width-5,rect3.y+5),(rect3.x+5,rect3.y+rect3.height-5),2)
	elif game_flag==1:
		pygame.draw.lines(WINDOW,red,False,[(rect3.x+3,rect3.y+14),(rect3.x+8,rect3.y+19),(rect3.x+21,rect3.y+7)],2)

	rect2=pygame.Rect(rect_state.left+rect_state.width-5-boxsize*2,rect_state.top+5,
		boxsize*2,boxsize)
	pygame.draw.rect(WINDOW,black,rect2)
	text_surface2=Font.render(str(int(time)),False,red)
	WINDOW.blit(text_surface2,rect2)

def draw_option_one(WINDOW,mousex,mousey,rect,str):
	if rect.collidepoint(mousex,mousey):
		pygame.draw.rect(WINDOW,deepskyblue,rect)
	Font2=pygame.font.SysFont('SimSun',option_height-2,bold=True)
	option_text_surface=Font2.render(str,True,black)
	WINDOW.blit(option_text_surface,rect)

def draw_option(WINDOW,mousex,mousey,option_flag):
	#global op
	if(option_flag==0):
		rect_option=pygame.Rect((2+30+2)*0+2,0,30,option_height)
		draw_option_one(WINDOW,mousex,mousey,rect_option,"选项")
		rect_Online=pygame.Rect((2+30+2)*1+2,0,30,option_height)
		draw_option_one(WINDOW,mousex,mousey,rect_Online,"联机")
	elif(option_flag==1):
		rect_junior=pygame.Rect((2+30+2)*0+2,0,30,option_height)
		rect_mid=pygame.Rect((2+30+2)*1+2,0,30,option_height)
		rect_senior=pygame.Rect((2+30+2)*2+2,0,30,option_height)
		rect_back=pygame.Rect((2+30+2)*3+2,0,30,option_height)
		draw_option_one(WINDOW,mousex,mousey,rect_junior,"初级")
		draw_option_one(WINDOW,mousex,mousey,rect_mid,"中级")
		draw_option_one(WINDOW,mousex,mousey,rect_senior,"高级")
		draw_option_one(WINDOW,mousex,mousey,rect_back,"返回")


def darw_map(level,WINDOW,WINDOWWIDTH,Font,flag_cnt,time,mousex,mousey,option_flag):

	#game option
	pygame.draw.polygon(WINDOW,white,[(0,option_height),
					(WINDOWWIDTH,option_height),
					(WINDOWWIDTH,option_height)])
	pygame.draw.rect(WINDOW,gray1,(0,0,WINDOWWIDTH,option_height))

	#option detail
	draw_option(WINDOW,mousex,mousey,option_flag)


	#Scoreboard
	pygame.draw.polygon(WINDOW,gray2,[(game_boundary,game_boundary+option_height),
					(game_boundary,game_boundary+state_height+option_height),
					(WINDOWWIDTH-game_boundary,game_boundary+option_height)])
	pygame.draw.polygon(WINDOW,white,[(game_boundary,game_boundary+state_height+option_height),
					(WINDOWWIDTH-game_boundary,game_boundary+option_height),
					(WINDOWWIDTH-game_boundary,game_boundary+state_height+option_height)])
	pygame.draw.rect(WINDOW,gray1,
		(game_boundary+1,game_boundary+option_height+1,WINDOWWIDTH-game_boundary*2-2,state_height-2))

	#state detail
	rect_state=pygame.Rect(game_boundary,game_boundary+option_height,WINDOWWIDTH-game_boundary*2,state_height)
	draw_state(rect_state,WINDOW,Font,flag_cnt,time)

	#draw the boxes
	for box_X in range(level):
		for box_Y in range(level):
			if(not clicked[box_X+1][box_Y+1]):
				x,y=get_xy(box_X,box_Y)
				pygame.draw.polygon(WINDOW,white,[(x-gapsize,y-gapsize),
					(x+boxsize+gapsize,y-gapsize),(x-gapsize,y+boxsize+gapsize)])
				pygame.draw.polygon(WINDOW,gray2,[(x+boxsize+gapsize,y+boxsize+gapsize),
					(x+boxsize+gapsize,y-gapsize),(x-gapsize,y+boxsize+gapsize)])
				pygame.draw.rect(WINDOW,gray1,(x,y,boxsize,boxsize))

def creat_mines(mines_map,prefix_sum,clicked,box_mines,rclicked,level,mines_number):
	#init
	for i in range(level+2):
		mines_map.append([0 for j in range(level+2)])
	for i in range(level+2):
		prefix_sum.append([0 for j in range(level+2)])
	for i in range(level+2):
		clicked.append([0 for j in range(level+2)])
	for i in range(level+2):
		box_mines.append([0 for j in range(level+2)])
	for i in range(level+2):
		rclicked.append([0 for j in range(level+2)])

	while sum(sum(row) for row in mines_map)!=mines_number:
		mines_map[random.randint(1,level)][random.randint(1,level)]=1
	#pprint.pprint(mines_map)
	for i in range(1,level+2):
		for j in range(1,level+2):
			prefix_sum[i][j]=prefix_sum[i-1][j]+prefix_sum[i][j-1]-prefix_sum[i-1][j-1]\
			+mines_map[i][j]
	#pprint.pprint(prefix_sum)
	for i in range(1,level+1):
		for j in range(1,level+1):
			fix=lambda x:0 if x<0 else x
			box_mines[i][j]=prefix_sum[i+1][j+1]-prefix_sum[fix(i-2)][j+1]-prefix_sum[i+1][fix(j-2)]\
			+prefix_sum[fix(i-2)][fix(j-2)]-mines_map[i][j] 
	#pprint.pprint(box_mines)

def get_box(mouse_x,mouse_y,level):
	for box_X in range(level):
		for box_Y in range(level):
			x,y=get_xy(box_X,box_Y)
			box_rect=pygame.Rect(x,y,boxsize,boxsize)
			if box_rect.collidepoint(mouse_x,mouse_y):
				return (box_X,box_Y)
	return (None,None)			

def box_flip(box_X,box_Y,box_mines,WINDOW,Font,level):

	if(0<=box_X<level and 0<=box_Y<level and not clicked[box_X+1][box_Y+1]):
		clicked[box_X+1][box_Y+1]=1
		if(mines_map[box_X+1][box_Y+1]):
			
			failure(WINDOW,level)
			return False
		x,y=get_xy(box_X,box_Y)
		pygame.draw.rect(WINDOW,gray2,(x-gapsize,y-gapsize,boxsize+2*gapsize,boxsize+2*gapsize))
		pygame.draw.rect(WINDOW,gray1,(x-gapsize+1,y-gapsize+1,boxsize+2*gapsize-2,boxsize+2*gapsize-2))
		if(box_mines[box_X+1][box_Y+1]):
			text_surface=Font.render(str(box_mines[box_X+1][box_Y+1]),False,
				chose_color.get(box_mines[box_X+1][box_Y+1],red),gray1)
			WINDOW.blit(text_surface,(x+5,y))
		else:
			xx=(-1,0,+1,-1,+1,-1,0,+1)
			yy=(-1,-1,-1,0,0,+1,+1,+1)
			for i in range(8):
				box_flip(box_X+xx[i],box_Y+yy[i],box_mines,WINDOW,Font,level)
	return True

def failure(WINDOW,level):
	global game_flag
	game_flag=2
	for box_X in range(level):
		for box_Y in range(level):
			if(mines_map[box_X+1][box_Y+1]):
				x,y=get_xy(box_X,box_Y)
				clicked[box_X+1][box_Y+1]=1
				pygame.draw.rect(WINDOW,red,(x-gapsize,y-gapsize,boxsize+2*gapsize,boxsize+2*gapsize))

if __name__ == "__main__":
	main()


