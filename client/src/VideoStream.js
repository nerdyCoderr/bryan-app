import { Paper } from "@mui/material";
import React, { useEffect, useState } from "react";

function VideoStream() {
  return (
    <Paper
      sx={{
        backgroundColor: "grey.800",
        color: "#fff",
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
      }}
    >
      {
        <img
          src="http://localhost:5000/video_feed"
          alt="Video Feed"
          style={{ width: "100%" }}
        />
      }
    </Paper>
  );
}

export default VideoStream;
