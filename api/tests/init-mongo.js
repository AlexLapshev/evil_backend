db.createUser(
    {
        user: "play_backend_user",
        pwd: "123456",
        roles: [
            {
                role: "readWrite",
                db: "play_backend_mongo"
            }
        ]
    }
)
