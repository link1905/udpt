import axios from "axios";
import { createAxiosConfig } from "../client.ts";

export const forumServiceClient = axios.create(createAxiosConfig("/forum/api"));

export interface CategoryFields {
  name: string;
}

export interface ThreadFields {
  title: string;
  content: string;
  creator_email: string;
  creator_name: string;
  created: string;
}

export interface CreateThreadForm {
  title: string;
  content: string;
  category?: number;
  parent?: number;
}
