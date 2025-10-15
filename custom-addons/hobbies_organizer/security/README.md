## Security rules

Access rules need the following information:
- id, name used as identifiers
- model_id:id, it's the name of the model, given like: model_"module"_"model"
- group_id:id, the group given permissions, e.g. base.group_user includes all logged in users
- perm_"read/write/create/unlink", permission for reading, modifying, creating and deleting a record