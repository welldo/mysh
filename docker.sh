docker run -dit \
  --name QingLong \
  --hostname QingLong \
  --restart always \
  -p 5700:5700 \
  -v /root/data:/ql/data \
  -v /root/data/config:/ql/data/config \
  whyour/qinglong:latest
