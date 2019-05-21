from yoyo import step

steps = [
  step("""
    CREATE TABLE `spotify_track` (
      `spotify_track_id` INT(11)  NOT NULL AUTO_INCREMENT PRIMARY KEY,
      `external_playlist_id` VARCHAR(50) DEFAULT NULL,
      `external_track_id` VARCHAR(50) NOT NULL,
      `create_slack_user_id` VARCHAR(50) DEFAULT NULL,
      `create_time` TIMESTAMP DEFAULT NOW(),
      CONSTRAINT UNIQUE INDEX `external_playlist_id_external_track_id` (`external_playlist_id`, `external_track_id`)
    ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4
  """,
       "DROP TABLE `spotify_track`")
]
