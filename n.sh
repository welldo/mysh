docker run -dit \
  --name nginx  \
  --hostname nginx  \
  --restart always \
  -p 80:80 \
  -p 81:81 \
  -p  443:443 \
  -v /root/nginx:/ql/data \
  -v /root/nginx/letsencrypt:/etc/letsencrypt \
  jc21/nginx-proxy-manager:latest
