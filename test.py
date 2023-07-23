from PIL import Image, ImageDraw, ImageFont

# Create a new image with a white background
img = Image.new('RGB', (400, 400), color='white')

# Create a drawing context
draw = ImageDraw.Draw(img)

# Set up some parameters
margin = 20
cell_size = (400 - margin * 2) // 7
day_font = ImageFont.truetype('font.ttc', 20)
header_font = ImageFont.truetype('font.ttc', 30)
schedule_font = ImageFont.truetype('font.ttc', 12)

# Draw the header
header_text = 'Monday, March 20'
header_width, header_height = draw.textsize(header_text, font=header_font)
header_x = (400 - header_width) // 2
header_y = margin
draw.text((header_x, header_y), header_text, fill='black', font=header_font)

# Draw the grid
for i in range(7):
    x = margin + i * cell_size
    y1 = margin + header_height + 10
    y2 = 400 - margin
    draw.line((x, y1, x, y2), fill='black')

for i in range(6):
    y = margin + header_height + 10 + i * cell_size
    x1 = margin
    x2 = 400 - margin
    draw.line((x1, y, x2, y), fill='black')

# Draw the day numbers
day_numbers = [str(i) for i in range(1, 32)]
day_number_x_offset = (cell_size - day_font.getsize('0')[0]) // 2
day_number_y_offset = (cell_size - day_font.getsize('0')[1]) // 2
for i, day_number in enumerate(day_numbers):
    row = i // 7
    col = i % 7
    x = margin + col * cell_size + day_number_x_offset
    y = margin + header_height + 10 + row * cell_size + day_number_y_offset
    draw.text((x, y), day_number, fill='black', font=day_font)

# Draw the schedule
schedule_x = margin
schedule_y = margin + header_height + 10 + cell_size * 6 + 10
schedule_width = 400 - margin * 2
schedule_height = cell_size
schedule_cell_width = schedule_width // 8
schedule_cell_height = schedule_height

# Draw time slots
start_time = 9
for i in range(8):
    time_text = f'{start_time}:00'
    time_width, time_height = draw.textsize(time_text, font=schedule_font)
    x = schedule_x + i * schedule_cell_width
    y = schedule_y
    draw.text((x, y), time_text, fill='black', font=schedule_font)
    start_time += 1

# Draw schedule cells
for i in range(8):
    for j in range(1):
        x = schedule_x + i * schedule_cell_width
        y = schedule_y + j * schedule_cell_height
        draw.rectangle((x, y, x + schedule_cell_width, y + schedule_cell_height), outline='black')

# Save the image
img.show()
