def clear_screen():
    # Check the operating system name
    if os.name == 'nt':
        # for Windows
        _ = os.system('cls')
    else:
        #  Linux/macOS
        _ = os.system('clear')