import axios from "axios";
import { createAxiosConfig } from "../client.ts";

export interface TagFields {
  name: string
}

export const tagServiceClient = axios.create(createAxiosConfig("/tag/api"));
