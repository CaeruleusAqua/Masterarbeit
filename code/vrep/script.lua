
simExtRemoteApiStart(19999,1300,false,true)

if simGetScriptExecutionCount() == 0 then
  console = simAuxiliaryConsoleOpen("Aux Console", 500, 0x10)
  oldprint = print
  print = function(...)
    simAuxiliaryConsolePrint(console, ...)
  end
end

threadFunction=function()
    while simGetSimulationState()~=sim_simulation_advancing_abouttostop do
        res,dist,dP,detectedObjectHandle=simReadProximitySensor(front_left_radar)
        if (res>0) then
            front_left_radar_dist=dist
        else
            front_left_radar_dist=max_dist
        end
        res,dist,dP,detectedObjectHandle=simReadProximitySensor(front_right_radar)
        if (res>0) then
            front_right_radar_dist=dist
        else
            front_right_radar_dist=max_dist
        end
        res,dist,dP,detectedObjectHandle=simReadProximitySensor(front_middle_radar)
        if (res>0) then
            front_middle_radar_dist=dist
        else
            front_middle_radar_dist=max_dist
        end
        res,dist,dP,detectedObjectHandle=simReadProximitySensor(back_left_radar)
        if (res>0) then
            back_left_radar_dist=dist
        else
            back_left_radar_dist=max_dist
        end
        res,dist,dP,detectedObjectHandle=simReadProximitySensor(back_right_radar)
        if (res>0) then
            back_right_radar_dist=dist
        else
            back_right_radar_dist=max_dist
        end

        x = simGetObjectPosition(roudabout,car )
        --print("Distance to Roundabout: ".. x[1]..", "..x[2]..", "..x[3].. "\n")
        --print("Distance to Roundabout: ".. math.sqrt(x[1]*x[1]+x[2]*x[2]).. "\n")

        roundabout_distance = math.sqrt(x[1]*x[1]+x[2]*x[2])
        x = simGetObjectPosition(enemy,car )
        --print("Distance to enemy: ".. x[1]..", "..x[2]..", "..x[3].. "\n")
        enemy_distance = math.sqrt(x[1]*x[1]+x[2]*x[2])
        enemy_intersection_distance = math.sqrt(-math.pow(roundabout_distance - raoundabout_diameter, 2) + math.pow(enemy_distance, 2))
        --print("r_dist, e_dist, ei_dist\n")
        --print(roundabout_distance-raoundabout_diameter.. "\n")
        --print(enemy_distance.. "\n")
        print(enemy_intersection_distance.. "\n")


        if oeid < 0 then
            oeid = enemy_intersection_distance
        else
            estimated_speed = (oeid - enemy_intersection_distance)/dt
            if enemy_car_speed < 0 then
                enemy_car_speed = estimated_speed
            else
                enemy_car_speed = 0.8 * enemy_car_speed + 0.2 * estimated_speed
            end
            oeid = enemy_intersection_distance
        end
        print("Enemy Speed: "..enemy_car_speed.."\n")

        if roundabout_distance-raoundabout_diameter < 2.3 and  roundabout_distance > 2.2  and front_left_radar_dist < 2.8 then
            print("activated\n")
            enemy_timewindow = enemy_intersection_distance / enemy_car_speed
            my_time_window = enemy_timewindow/2

            deltav = max_speed - speed
            t = deltav/accel
            if my_time_window -t < 0 then
                s=(accel/2)*my_time_window*my_time_window + speed * my_time_window
            else
                s = ((accel/2)*t*t + speed * t) +  (my_time_window-t)*speed
            end
            if s >= roundabout_distance-raoundabout_diameter then
                target_speed = max_speed
                print("start1\n")
            else
                target_speed = 0
                print("stop1\n")
            end
        else
            target_speed = max_speed
        end






        --if roundabout_distance < 2.4 and  roundabout_distance > 2.2  and front_left_radar_dist < 1.8 then
            --target_speed = 0
        --    print("brake\n")
        --else
        --    target_speed = max_speed
        --end

        length = length + speed*dt
        dv=accel*dt
        if speed+dv <= target_speed then
            speed = speed + dv
        end

        if speed > target_speed then
             dv=neg_accel*dt
            speed = speed - dv
        end


        path_length = simGetPathLength(goal_path)
        newPos = simGetPositionOnPath(goal_path,(length/path_length)%1)
        newRot = simGetOrientationOnPath(goal_path,(length/path_length)%1)
        newPos[3] = simGetObjectPosition(carFrame,-1)[3]

        simSetObjectOrientation(carFrame,-1,newRot)
        simSetObjectPosition(carFrame,-1,newPos)

        -- Since this script is threaded, don't waste time here:
        simSwitchThread() -- Resume the script at next simulation loop start
    end
end



-- Put some initialization code here:
front_left_radar=simGetObjectHandle('front_left_radar')
front_right_radar=simGetObjectHandle('front_right_radar')
front_middle_radar=simGetObjectHandle('front_middle_radar')
back_left_radar=simGetObjectHandle('back_left_radar')
back_right_radar=simGetObjectHandle('back_right_radar')
roudabout = simGetObjectHandle('Roundabout')
car = simGetObjectHandle('Anchor')
carFrame = simGetObjectHandle('mycar')
goal_path = simGetObjectHandle('car_path')
enemy =  simGetObjectHandle('enemy_car1')


desiredSteeringAngle=0
desiredWheelRotSpeed=200*math.pi/180
d=0.755 -- 2*d=distance between left and right wheels
l=2.5772 -- l=distance between front and read wheels
speed = 0.83
target_speed = 0.83
max_speed = 0.83
length = 0
dt = 0.05
accel = 0.34
neg_accel = 1.1
max_dist=30
enemy_car_speed = -1
raoundabout_diameter = 2
oeid = 0


-- Here we execute the regular thread code:
res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
    simAddStatusbarMessage('Lua runtime error: '..err)
end

-- Put some clean-up code here:
