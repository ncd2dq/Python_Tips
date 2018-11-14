
msg = ''
new_line = ''
while new_line != 'q':
    new_line = input()
    if new_line == 'q':
        break
    msg += '\n' + new_line


with open('your_output.py', 'w') as file:
    file.write(msg)

    
