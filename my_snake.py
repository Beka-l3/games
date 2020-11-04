import random
import curses
import time

s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh, sw, 0 ,0)
w.keypad(1)
w.timeout(100)

bx = sw/3
by = sh/4
sx = 1*bx
sy = by*2


def print_border(flag):
	for i in range(2):
		for j in range(sx+1):
			if i == 0:
				if flag == 0:
					w.addch(by, bx + j, '-')
				if flag == 1:
					w.addch(by, bx + j, '@')
			if i == 1:
				if flag == 0:
					w.addch(by+sy, bx + j, '-')
				if flag == 1:
					w.addch(by+sy, bx + j, '@')

		for j in range(sy-1):
			if i == 0:
				if flag == 0:
					w.addch(by + j + 1, bx, '|')
				if flag == 1:
					w.addch(by + j + 1, bx, '@')
			if i == 1:
				if flag == 0:
					w.addch(by + j + 1, bx+sx, '|')
				if flag == 1:
					w.addch(by + j + 1, bx+sx, '@')


def print_mess(mess, my, mx):
	messlen = len(mess)
	for i in range(messlen):
		w.addch(my, mx + i, mess[i])


def menu():
	print_mess("SNAKE", sh/2 - 5, sw/2 - 5)
	print_mess("Press KEY_RIGHT instead of ENTER", sh/2 + 10, sw/2 - 17)
	print_mess("Made by Bekzhan Talgat", sh-2, sw/2 - 12)

	pointer = [sh/2 - 2, sw/2 - 7]
	position = 0

	while True:
		key = w.getch()
		
		print_mess('>', pointer[0] + position, pointer[1])
		print_mess('classic', sh/2 - 2, sw/2 - 5)
		print_mess('portal border', sh/2 - 1, sw/2 - 5)
		print_mess('exit', sh/2 - 0, sw/2 - 5)

		if key == curses.KEY_DOWN:
			print_mess(' ', pointer[0] + position, pointer[1])
			position = (position + 1) if position < 2 else 0

		if key == curses.KEY_UP:
			print_mess(' ', pointer[0] + position, pointer[1])
			position = (position - 1) if position > 0 else 2

		if key == curses.KEY_RIGHT:
			return position


def game(flag):
	w.clear()
	print_border(flag)

	snk_x = 3*sw/7
	snk_y = sh/2
	snake = [
		[snk_y, snk_x],
		[snk_y, snk_x - 1],
		[snk_y, snk_x - 2]
	]

	food = [sh/2, sw/2]
	w.addch(food[0], food[1], 'o')
	
	score = [3, by, bx + sx + 5]
	print_mess(str(score[0]), score[1], score[2])

	key = curses.KEY_RIGHT

	while True:
		next_key = w.getch()
		key = key if next_key == -1 else next_key
		teleported = False

		new_head = [snake[0][0], snake[0][1]]

		if key == curses.KEY_DOWN:
			new_head[0] += 1
		if key == curses.KEY_UP:
			new_head[0] -= 1
		if key == curses.KEY_LEFT:
			new_head[1] -= 1
		if key == curses.KEY_RIGHT:
			new_head[1] += 1

		if flag == 0:
			if snake[0][0] in [by, by+sy] or snake[0][1] in [bx, bx+sx] or snake[0] in snake[1:]:
				w.clear()
				break
		elif flag == 1:
			if snake[0] in snake[1:]:
				w.clear()
				break
			if snake[0][0] == by:
				new_head = [by+sy - 1, snake[0][1]]
				teleported = True
			if snake[0][0] == by+sy:
				new_head = [by + 1, snake[0][1]]
				teleported = True
			if snake[0][1] == bx:
				new_head = [snake[0][0], bx+sx - 1]
				teleported = True
			if snake[0][1] == bx+sx:
				new_head = [snake[0][0], bx + 1]
				teleported = True

		snake.insert(0, new_head)

		if snake[0] == food:
			# curses.beep()
			score[0] += 1
			print_mess(str(score[0]), score[1], score[2])

			food = None
			while food == None:
				nf = [
					random.randint(by+1, by+sy-1),
					random.randint(bx+1, bx+sx-1)
				]
				food = nf if nf not in snake else None
			w.addch(food[0], food[1], 'o')
		else:
			tail = snake.pop()
			w.addch(tail[0], tail[1], ' ')
			if tail[0] in [by, by+sy] or tail[1] in [bx, bx+sx]:
				w.addch(tail[0], tail[1], '@')

		w.addch(snake[0][0], snake[0][1], '*')


while True:
	flag = menu()

	if flag == 2:
		curses.endwin()
		quit()

	game(flag)

