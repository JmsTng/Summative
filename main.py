import time
start=time.time()
while True:print(f'You were away for {round(time.time()-start,2):,} seconds!',end='\r')