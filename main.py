#vacuum cleaner agent

#Mode 1: The agent can sense Clean or dirty of his room
#Mode 2: The agent can sense Clean or dirty of his room and neighbor rooms
#Mode 3: The agent can sense Clean or dirty of all rooms

mode = 3

if mode == 1:
    import one
elif mode == 2:
    import three
elif mode == 3:
    import all