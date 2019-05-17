#!/usr/bin/env roseus

(ros::roseus "pepper_twitter_client")

(ros::advertise "/pepper_tweet" std_msgs::String 1)

(defun tweet (str &rest args)
  (ros::publish "/pepper_tweet" (instance std_msgs::String :init :data (apply #'format nil str args))))

(defun main ()
  (unix:sleep 3)
  (let (robot-name tweet-sentence)
    (setq robot-name (ros::get-param "robot_name"))
    (setq tweet-sentence (concatenate string "おはよう\n" robot-name "より"))
    (tweet tweet-sentence)
    ))

(progn (main) (exit))
