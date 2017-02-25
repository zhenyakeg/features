from tkinter import Tk, Canvas, BOTH

window = Tk()
window.wm_state('zoomed')
window.title('Game of Life')
canvas = Canvas(window, bg='white')
canvas.pack(fill=BOTH, expand=1)
block_width = 10
additions = -block_width, 0, block_width


class Block:
    color = 'black'

    def __init__(self, cords=(0, 0)):
        self.x, self.y = cords
        self.id = canvas.create_rectangle(self.x, self.y, self.x + block_width, self.y + block_width, fill=self.color)
        canvas.coords(self.id, self.x, self.y, self.x + block_width, self.y + block_width)
        canvas.itemconfig(self.id, fill=self.color)

    def remove(self, blocks):
        canvas.delete(self.id)
        del blocks[(self.x, self.y)]

    def define_existing_life(self, blocks, deleted_blocks, near_blocks):
        counter = 0
        for add1 in additions:
            for add2 in additions:
                if not add1 == 0 == add2:
                    if (self.x + add1, self.y + add2) in blocks:
                        counter += 1
                    else:
                        near_blocks.add((self.x + add1, self.y + add2))
        if not 2 <= counter <= 3:
            deleted_blocks.add((self.x, self.y))

using_blocks, creation_queue, time_flow, escape = {}, None, False, False


def game():
    global creation_queue, time_flow, escape, using_blocks
    screen, iterator = canvas.create_text(100, 50, font='Times'), 0
    canvas.focus_set()
    while not escape:
        canvas.itemconfig(screen, text='Iterations: ' + str(iterator))
        iterator += 1
        near_blocks, deleted_blocks, born_blocks = set(), set(), set()
        check_and_rebuild(using_blocks, near_blocks, deleted_blocks, born_blocks)
        canvas.update(), canvas.bind('<KeyPress>', button_press_handler)
        while not time_flow and not escape:
            canvas.bind('<Button-1>', creation)
            if creation_queue:
                using_blocks[creation_queue] = Block(creation_queue)
                creation_queue = None
            canvas.update(), canvas.bind('<KeyPress>', button_press_handler)


def creation(event):
    global creation_queue
    cords = (event.x_root - event.x_root % block_width, event.y_root - event.y_root % block_width - 25)
    if cords not in using_blocks:
        creation_queue = cords


def button_press_handler(event):
    global time_flow, escape
    if event.keysym == 'space':
        time_flow ^= True
    elif event.keysym == 'Escape':
        escape = True


def check_and_rebuild(blocks, near_blocks, deleted_blocks, born_blocks):
    for block in blocks.values():
        block.define_existing_life(blocks, deleted_blocks, near_blocks)
    for block in near_blocks:
        define_new_life(block, blocks, born_blocks)
    for block in deleted_blocks:
        blocks[block].remove(blocks)
    for block in born_blocks:
        blocks[block] = Block(block)


def define_new_life(block, blocks, born_blocks):
    counter = 0
    for add1 in additions:
        for add2 in additions:
            if not add1 == 0 == add2 and (block[0] + add1, block[1] + add2) in blocks:
                counter += 1
    if counter == 3:
        born_blocks.add(block)
game()
