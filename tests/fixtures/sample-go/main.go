package main

import "net/http"

func main() {
	http.HandleFunc("/users", usersHandler)
	http.ListenAndServe(":8080", nil)
}

func usersHandler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("users"))
}
