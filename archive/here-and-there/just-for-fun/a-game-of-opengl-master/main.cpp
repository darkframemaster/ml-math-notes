#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>
#include <cmath>
#include <ctime>
#include <vector>
#include<cstdio>
#include<stdio.h>
#include<iostream>
#include<cstring>
#include<time.h>

#define WindowWidth   400
#define WindowHeight 400
#define WindowTitle  "迷宫"


using namespace std;

static const GLfloat half_width=0.3f;
static const GLfloat step_width=half_width;

static const GLfloat red_color[] = {1.0f, 0.0f, 0.0f, 1.0f};
static const GLfloat green_color[] = {0.0f, 1.0f, 0.0f, 0.3333f};
static const GLfloat blue_color[] = {0.0f, 0.0f, 1.0f, 0.5f};


GLfloat DEFAULT_MAP_POINT[][2]={-4.0f,8.0f,-4.0f,0.0f,
                                -8.0f,-4.0f,4.0f,-4.0f,
                                4.0f,-4.0f,4.0f,4.0f,
                              	-8.0f,8.0f,8.0f,8.0f,
                                8.0f,8.0f,8.0f,-8.0f,
                                8.0f,-8.0f,-8.0f,-8.0f,
                                -8.0f,-8.0f,-8.0f,8.0f};



void setLight(void)
{
	static const GLfloat light_position[] = {1.0f, 1.0f, -1.0f, 1.0f};
	static const GLfloat light_ambient[] = {0.2f, 0.2f, 0.2f, 1.0f};
	static const GLfloat light_diffuse[] = {1.0f, 1.0f, 1.0f, 1.0f};
	static const GLfloat light_specular[] = {1.0f, 1.0f, 1.0f, 1.0f};
	glLightfv(GL_LIGHT0, GL_POSITION, light_position);
	glLightfv(GL_LIGHT0, GL_AMBIENT,light_ambient);
	glLightfv(GL_LIGHT0, GL_DIFFUSE,light_diffuse);
	glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular);
	glEnable(GL_LIGHT0);
	glEnable(GL_LIGHTING);
	glEnable(GL_DEPTH_TEST);
}
void setMatirial(const GLfloat mat_diffuse[4], GLfloat mat_shininess)
{
    static const GLfloat mat_specular[] = {0.0f, 0.0f, 0.0f, 1.0f};
	static const GLfloat mat_emission[] = {0.0f, 0.0f, 0.0f, 1.0f};
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, mat_diffuse);
	glMaterialfv(GL_FRONT, GL_SPECULAR,mat_specular);
	glMaterialfv(GL_FRONT, GL_EMISSION, mat_emission);
	glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess);
}

GLfloat lookat_x;
GLfloat lookat_y;
GLfloat lookat_z=1;

class point{
public:
        GLfloat position_x;
        GLfloat position_y;
        point(){}
        point(int x,int y):position_x(x),position_y(y){}
        void setposition(int x,int y){
                position_x=x;position_y=y;
        }
        void cout_point(){
            cout<<"("<<position_x<<','<<position_y<<")";
        }
};
class line{
public:
    point point_start;
    point point_end;
    char type;

    line(){}
    line(point s,point e){
        if(s.position_x==e.position_x){//如果x轴的坐标相同那么就是竖线，然后看他们的y坐标决定它们的 前后顺序
                type='|';
                if(s.position_y<e.position_y){
                        point_start=s;
                        point_end=e;
                }
                else{
                    point_start=e;
                    point_end=s;
                }
        }
        else{//x不相等 那么y肯定相等 不要吐槽简单的设定
            type='-';
            if(s.position_x<e.position_x){
                point_start=s;
                point_end=e;
            }
            else{
                point_end=s;
                point_start=e;
            }
        }
    }

    void set_point(GLfloat x1,GLfloat y1,GLfloat x2,GLfloat y2){
        if(x1==x2){//如果x轴的坐标相同那么就是竖线，然后看他们的y坐标决定它们的 前后顺序
                type='|';
                if(y1<y2){
                        point_start.position_x=x1;point_start.position_y=y1;
                        point_end.position_x=x2;point_end.position_y=y2;
                }
                else{
                        point_start.position_x=x2;point_start.position_y=y2;
                        point_end.position_x=x1;point_end.position_y=y1;
                }
        }
        else if(y1==y2){//x不相等 那么y肯定相等 不要吐槽简单的设定
            type='-';
            if(x1<x2){
                    point_start.position_x=x1;point_start.position_y=y1;
                    point_end.position_x=x2;point_end.position_y=y2;
            }
            else{
                    point_start.position_x=x2;point_start.position_y=y2;
                    point_end.position_x=x1;point_end.position_y=y1;
            }
        }
        else{
            cout<<"what the fuck!!!"<<endl;
        }
    }
    void cout_line(){
        this->point_start.cout_point();
        cout<<"->";
        this->point_end.cout_point();
    }
};
class player{//玩家类
public:
    string name;
    point player_position;

    player(){
        cout<<"input a player name:"<<endl;
        cin>>name;
        cout<<endl<<"welcome"<<name<<endl;
        player_position.position_x=-7.0f;
        player_position.position_y=-7.0f;
        //lookat_x=player_position.position_x;
        //lookat_y=player_position.position_y;
    }
    player(string n){
            name=n;
    }
    bool if_arrive(point map_end){//判断玩家是否到达
            if(player_position.position_x-half_width<map_end.position_x&&map_end.position_x<player_position.position_x+half_width&&player_position.position_y-half_width<map_end.position_y&&map_end.position_y<player_position.position_y+half_width){
                return true;
            }
            else
                return false;
    }
    void display(){
            lookat_x=player_position.position_x;
            lookat_y=player_position.position_y;
            setMatirial(green_color, 30.0);
            glBegin(GL_POLYGON);
            glVertex3f(player_position.position_x-half_width,player_position.position_y+half_width,0.0f);
            glVertex3f(player_position.position_x+half_width,player_position.position_y+half_width,0.0f);
            glVertex3f(player_position.position_x+half_width,player_position.position_y-half_width,0.0f);
            glVertex3f(player_position.position_x-half_width,player_position.position_y-half_width,0.0f);
            glEnd();
    }
    void cout_player_position(){
        cout<<"("<<this->player_position.position_x<<','<<this->player_position.position_y<<')';
    }
    GLfloat get_position_x(){
        return player_position.position_x;
    }
    GLfloat get_position_y(){
        return player_position.position_y;
    }
}test_person;

class game_map{//地图类
public:

    string map_name;
    int lines_number;
    line* map_line;
    point map_end;

    game_map(){//默认地图
        map_name="map1";
        lines_number=7;
        map_line=new line[lines_number];
        for(int i=0;i<lines_number;i++){
            map_line[i].set_point(DEFAULT_MAP_POINT[i*2][0],DEFAULT_MAP_POINT[i*2][1],DEFAULT_MAP_POINT[i*2+1][0],DEFAULT_MAP_POINT[i*2+1][1]);

            map_line[i].cout_line();
            cout<<endl<<'('<<DEFAULT_MAP_POINT[i*2][0]<<','<<DEFAULT_MAP_POINT[i*2][1]<<')'<<"    "<<'('<<DEFAULT_MAP_POINT[i*2+1][0]<<','<<DEFAULT_MAP_POINT[i*2+1][1]<<')'<<endl;
        }
        map_end.position_x=-6.0;
        map_end.position_y=6.0;
    }
    game_map(int n){
    }
    bool if_touch(point player){
        int i=0,j=0;
        for(i=0;i<lines_number;i++){
            test_person.cout_player_position();
            cout<<endl;
                if(map_line[i].type=='-'){
                        if(map_line[i].point_start.position_x<=test_person.get_position_x()+half_width&&test_person.get_position_x()-half_width<=map_line[i].point_end.position_x)
                        {
                            if(test_person.get_position_y()-half_width<map_line[i].point_start.position_y&&map_line[i].point_start.position_y<test_person.get_position_y()+half_width){
                                return true;
                            }
                        }
                }
                else if(map_line[i].type=='|'){
                     if(map_line[i].point_start.position_y<=test_person.get_position_y()+half_width&&test_person.get_position_y()-half_width<=map_line[i].point_end.position_y)
                        {
                            if(test_person.get_position_x()-half_width<map_line[i].point_start.position_x&&map_line[i].point_start.position_x<test_person.get_position_x()+half_width){
                                return true;
                            }
                        }
                }
                else{
                    cout<<"oh my god!!!"<<endl;
                }
        }
        return false;
    }
    void display(){
        for(int i=0;i<lines_number;i++){
            glBegin(GL_LINES);
            glVertex3f(map_line[i].point_start.position_x,map_line[i].point_start.position_y,0);
            glVertex3f(map_line[i].point_end.position_x,map_line[i].point_end.position_y,0);
            glEnd();
        }//城墙

        glBegin(GL_LINES);
        glVertex3f(map_end.position_x-half_width,map_end.position_y-half_width,0);
        glVertex3f(map_end.position_x+half_width,map_end.position_y+half_width,0);
        glVertex3f(map_end.position_x-half_width,map_end.position_y+half_width,0);
        glVertex3f(map_end.position_x+half_width,map_end.position_y-half_width,0);
        glEnd();//终点
    }
    ~game_map(){
        delete []   map_line;
    }
}test_map;


void display(void)
{
	// 清除屏幕
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    setLight();
    gluLookAt(lookat_x,lookat_y,10*half_width, lookat_x, lookat_y, 0, 0, 1, 0);
    //cout<<'('<<lookat_x<<','<<lookat_y<<')'<<endl;
    test_map.display();
	test_person.display();
	// 设置视角
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(75, 1, 1, 21);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();


	glFlush();

	// 交换缓冲区，并保存像素数据到文件
	glutSwapBuffers();
//	grab();
}
void myIdle(void){

    display();
    if(test_person.if_arrive(test_map.map_end)==true){
        cout<<"you make it!"<<endl;
        test_person.player_position.position_x=-7.0f;test_person.player_position.position_y=-7.0f;
        return ;
    }
}

void keyboard(unsigned char key, int x, int y) {
    switch (key) {
        case 'w':
            test_person.player_position.position_y+=step_width;
            lookat_y+=step_width;
            if(test_map.if_touch(test_person.player_position)){cout<<"touch"<<endl;test_person.player_position.position_y-=step_width;lookat_y-=step_width;}
            break;
        case 'a':
            test_person.player_position.position_x-=step_width;
            lookat_x-=step_width;
             if(test_map.if_touch(test_person.player_position)){cout<<"touch"<<endl;test_person.player_position.position_x+=step_width;lookat_x+=step_width;}
            break;
        case 's':
            test_person.player_position.position_y-=step_width;
            lookat_y-=step_width;
             if(test_map.if_touch(test_person.player_position)){cout<<"touch"<<endl;test_person.player_position.position_y+=step_width;lookat_y+=step_width;}
            break;
        case 'd':
            test_person.player_position.position_x+=step_width;
            lookat_x+=step_width;
             if(test_map.if_touch(test_person.player_position)){cout<<"touch"<<endl;test_person.player_position.position_x-=step_width;lookat_x-=step_width;}
            break;
        case 27:
            exit(0);
            break;
        default:
            break;
    }
}


int main(int argc, char* argv[])
{

	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowPosition(100, 100);
	glutInitWindowSize(WindowWidth, WindowHeight);
	glutCreateWindow(WindowTitle);


	glutDisplayFunc(&display);
	 glutKeyboardFunc(keyboard);
	glutIdleFunc(&myIdle);

	// 在这里做一些初始化
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_TEXTURE_2D);

	// 开始显示
	glutMainLoop();

    return 0;
}

