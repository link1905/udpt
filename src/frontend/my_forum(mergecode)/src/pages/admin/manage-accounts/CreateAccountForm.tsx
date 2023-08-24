import React, { useState } from "react";
import { Input, Button, Paper } from "@mantine/core";
import { requestSignUp } from "../../../services/account/signup";

const CreateAccountForm = () => {
  const [formData, setFormData] = useState({
    username: "",
    password1: "",
    password2: "",
    email: "",
    first_name: "",
    last_name: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    requestSignUp(formData)
      .then(() => {
        // Account created successfully, perform any necessary actions
        console.log("Account created successfully");
      })
      .catch((error) => {
        console.error("Error creating account:", error);
      });
  };

  return (
    <Paper padding="lg">
      <form onSubmit={handleSubmit}>
        <Input
          placeholder="Username"
          name="username"
          value={formData.username}
          onChange={handleChange}
        />
        <Input
          type="password"
          placeholder="Password"
          name="password1"
          value={formData.password1}
          onChange={handleChange}
        />
        <Input
          type="password"
          placeholder="Confirm Password"
          name="password2"
          value={formData.password2}
          onChange={handleChange}
        />
        <Input
          type="email"
          placeholder="Email"
          name="email"
          value={formData.email}
          onChange={handleChange}
        />
        <Input
          placeholder="First Name"
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
        />
        <Input
          placeholder="Last Name"
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
        />
        <Button type="submit" color="blue" style={{ marginTop: "10px" }}>
          Create Account
        </Button>
      </form>
    </Paper>
  );
};

export default CreateAccountForm;
