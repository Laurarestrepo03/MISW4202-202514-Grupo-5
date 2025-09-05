for i in {1..100}; do
  echo "Request $i"
  time curl -w "HTTP Response Code: %{http_code}\n" http://localhost:8000/orders
  echo "--"
done
