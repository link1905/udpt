import axios from "axios";
import { createAxiosConfig } from "../client.ts";

export const accountServiceClient = axios.create(
  createAxiosConfig("/account/api"),
);

export interface AccountFields {
  avatar: string;
  date_joined: string;
  email: string;
  first_name: string;
  last_name: string;
  username: string;
  is_staff: boolean;
}
export interface CreateAccountRequestBody {
  username: string;
  password1: string;
  password2: string;
  email: string;
  first_name: string;
  last_name: string;
}
