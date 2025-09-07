start_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "Start time: $start_time"
for i in {1..1}; do
  echo "Request $i"
  time curl -w "HTTP Response Code: %{http_code}\n" http://localhost:8000/orders
  echo "--"
done
end_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "End time: $end_time"
