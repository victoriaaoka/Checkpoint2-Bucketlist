from marshmallow import Schema, fields, validate


class UserRegistrationSchema(Schema):

    username = fields.String(validate=[validate.Length(min=3),
                              validate.Regexp(r"[a-zA-Z0-9_\- ]*$",
                                              error="Invalid characters entered.")],
                              required=True,
                              error_messages={"required": "Please enter a username"})
    email = fields.Email(validate=[validate.Length(max=30)],
                         required=True,
                         error_messages={"required": "Please enter an email address"})
    password = fields.String(validate=[validate.Length(min=6)],
                             required=True,
                             error_messages={"required": "Please enter a password"})


class UserLoginSchema(Schema):

    username = fields.String(validate=[validate.Length(min=3),
                        validate.Regexp(r"[a-zA-Z0-9_\- ]*$",
                                              error="Invalid characters entered.")],
                              required=True,
                              error_messages={"required": "Please enter a username"})
    password = fields.String(validate=[validate.Length(min=5)],
                             required=True,
                             error_messages={"required": "Enter password"})


class BucketlistSchema(Schema):

    name = fields.String(validate=[validate.Length(min=3),
                                        validate.Regexp(r"[a-zA-Z0-9_\- ]*$",
                                         error="Invalid characters")],
                         required=True,
                         error_messages={"required": "Please enter the bucketlist name"})


class BucketlistItemSchema(Schema):

    name = fields.String(validate=[validate.Length(min=3),
                                        validate.Regexp(r"[a-zA-Z0-9_\- ]*$",
                                         error="Invalid characters")],
                         required=True,
                         error_messages={"required": "Please enter an item name"})
