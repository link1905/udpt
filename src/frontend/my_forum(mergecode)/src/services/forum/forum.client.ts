import axios from "axios";
import { createAxiosConfig } from "../client.ts";

export const forumServiceClient = axios.create(createAxiosConfig("/forum/api"));

export interface CategoryFields {
  name: string;
  created: string;
}

export interface ThreadFields {
  title: string;
  content: string;
  creator_id: number;
  creator_name: string;
  creator_email: string;
  parent: number;
  approved: boolean;
  approver_id: number;
  approver_name: string;
  approver_email: string;
  created: string;
  updated: string;
  thread: number;
}

export interface CreateThreadForm {
  title: string;
  content: string;
  category?: number;
  parent?: number;
}
export interface CreateThreadVoteData {
  thread: number
  is_upvote: boolean
}

export interface UpdateThread {
  title: string;
  content: string;
  approved: boolean;
}
export interface TaggedThreadFields {
  tag_id: number;
  tag_name: string;
  thread_id: number;
}

export interface ThreadVoteFields {
  thread: number
  is_upvote: boolean
  user_id: number
}
