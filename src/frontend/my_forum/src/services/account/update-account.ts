import { accountServiceClient } from "./account.client.ts";

export interface AccountFormData {
  id: number;
  username: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  password1?: string;
  password2?: string;
  avatar?: File;
}
export async function requestUpdateAccount({ id, ...values }: AccountFormData) {
  const formData = new FormData();
  Object.entries(values).map(([key, value]) => {
    if (value) {
      formData.append(key, value);
    }
  });
  const { data } = await accountServiceClient.put(
    `/models/users/records/${id}/`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    },
  );
  return data;
}
