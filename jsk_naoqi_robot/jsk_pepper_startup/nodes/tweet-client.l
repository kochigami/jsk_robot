#!/usr/bin/env roseus

(ros::roseus "pepper_twitter_client")

(ros::advertise "/pepper_tweet" std_msgs::String 1)

(defun tweet (str &rest args)
  (ros::publish "/pepper_tweet" (instance std_msgs::String :init :data (apply #'format nil str args))))

(defun main (robot-name)
  (unix:sleep 3)
  (let (tweet-sentence)
    (print robot-name) ;; nil
    (setq tweet-sentence (concatenate string "おはよう  " robot-name "より"))
    (tweet tweet-sentence) "おはよう  より"
    ))

(progn
  ;; [ERROR] [1558160797.405924316]: unknown ros::param::get, key=robot_name
  (setq robot-name (ros::get-param "robot_name"))
  (print robot-name) ;; nil
  (main robot-name)
  (exit))
