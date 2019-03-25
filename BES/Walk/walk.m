clear
clc

f = fopen('walk_1.txt','r');
r1y = [];
while ~feof(f) % 判斷是否為文件末尾
    r1y = [r1y, fscanf(f,"%f")];
end
fclose(f);

f = fopen('walk_2.txt','r');
r2y = [];
while ~feof(f) % 判斷是否為文件末尾
    r2y = [r2y, fscanf(f,"%f")];
end
fclose(f);

f = fopen('walk_3.txt','r');
r3y = [];
while ~feof(f) % 判斷是否為文件末尾
    r3y = [r3y, fscanf(f,"%f")];
end
fclose(f);

f = fopen('walk_4.txt','r');
r4y = [];
while ~feof(f) % 判斷是否為文件末尾
    r4y = [r4y, fscanf(f,"%f")];
end
fclose(f);

f = fopen('walk_5.txt','r');
r5y = [];
while ~feof(f) % 判斷是否為文件末尾
    r5y = [r5y, fscanf(f,"%f")];
end
fclose(f);


f = fopen('walk_6.txt','r');
r6y = [];
while ~feof(f) % 判斷是否為文件末尾
    r6y = [r6y, fscanf(f,"%f")];
end
fclose(f);


f = fopen('walk_7.txt','r');
r7y = [];
while ~feof(f) % 判斷是否為文件末尾
    r7y = [r7y, fscanf(f,"%f")];
end
fclose(f);

f = fopen('walk_8.txt','r');
r8y = [];
while ~feof(f) % 判斷是否為文件末尾
    r8y = [r8y, fscanf(f,"%f")];
end
fclose(f);


f = fopen('walk_9.txt','r');
r9y = [];
while ~feof(f) % 判斷是否為文件末尾
    r9y = [r9y, fscanf(f,"%f")];
end
fclose(f);


f = fopen('walk_10.txt','r');
r10y = [];
while ~feof(f) % 判斷是否為文件末尾
    r10y = [r10y, fscanf(f,"%f")];
end
fclose(f);


f = fopen('time_walk_1.txt','r');
r1x = [];
while ~feof(f) % 判斷是否為文件末尾
    r1x = [r1x, fscanf(f,"%f")];
end
fclose(f);


f = fopen('time_walk_2.txt','r');
r2x = [];
while ~feof(f) % 判斷是否為文件末尾
    r2x = [r2x, fscanf(f,"%f")];
end
fclose(f);

f = fopen('time_walk_3.txt','r');
r3x = [];
while ~feof(f) % 判斷是否為文件末尾
    r3x = [r3x, fscanf(f,"%f")];
end
fclose(f);

f = fopen('time_walk_4.txt','r');
r4x = [];
while ~feof(f) % 判斷是否為文件末尾
    r4x = [r4x, fscanf(f,"%f")];
end
fclose(f);

f = fopen('time_walk_5.txt','r');
r5x = [];
while ~feof(f) % 判斷是否為文件末尾
    r5x = [r5x, fscanf(f,"%f")];
end
fclose(f);


f = fopen('time_walk_6.txt','r');
r6x = [];
while ~feof(f) % 判斷是否為文件末尾
    r6x = [r6x, fscanf(f,"%f")];
end
fclose(f);


f = fopen('time_walk_7.txt','r');
r7x = [];
while ~feof(f) % 判斷是否為文件末尾
    r7x = [r7x, fscanf(f,"%f")];
end
fclose(f);

f = fopen('time_walk_8.txt','r');
r8x = [];
while ~feof(f) % 判斷是否為文件末尾
    r8x = [r8x, fscanf(f,"%f")];
end
fclose(f);

f = fopen('time_walk_9.txt','r');
r9x = [];
while ~feof(f) % 判斷是否為文件末尾
    r9x = [r9x, fscanf(f,"%f")];
end
fclose(f);

f = fopen('time_walk_10.txt','r');
r10x = [];
while ~feof(f) % 判斷是否為文件末尾
    r10x = [r10x, fscanf(f,"%f")];
end
fclose(f);

figure(1)
plot(r1x,r1y)
axis([0,0.15,-0.05,0.15])

figure(2)
plot(r2x,r2y)
axis([0,0.15,-0.05,0.15])

figure(3)
plot(r3x,r3y)
axis([0,0.15,-0.05,0.15])

figure(4)
plot(r4x,r4y)
axis([0,0.15,-0.05,0.15])

figure(5)
plot(r5x,r5y)
axis([0,0.15,-0.1,0.2])

figure(6)
plot(r6x,r6y)
axis([0,0.15,-0.05,0.15])

figure(7)
plot(r7x,r7y)
axis([0,0.15,-0.05,0.15])

figure(8)
plot(r8x,r8y)
axis([0,0.15,-0.05,0.15])

figure(9)
plot(r9x,r9y)
axis([0,0.15,-0.05,0.15])

figure(10)
plot(r10x,r10y)
axis([0,0.15,-0.05,0.15])