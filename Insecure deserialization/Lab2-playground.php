<?php

class User {
    public string $username;
    // public string $access_token
    public int $access_token;

    public function __construct(string $username, int $access_token){
        $this->username = $username;
        $this->access_token = $access_token;
    }
}

// $user = new User("wiener", "randombits");
$user = new User("wiener", 0);

echo serialize($user);