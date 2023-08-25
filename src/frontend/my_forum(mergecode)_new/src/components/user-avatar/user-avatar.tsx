import { Avatar, Group } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import {
  requestGetDetailAccount,
  requestGetDetailAccountKeys,
} from "../../services/account/account-detail.ts";

export function UserAvatar({ id }: { id: number }) {
  const { data } = useQuery(requestGetDetailAccountKeys(id), () =>
    requestGetDetailAccount(id),
  );
  return (
    <Group>
      <Avatar
        src={`${import.meta.env.VITE_API_URL}account/media/${data?.fields
          ?.avatar}`}
        color="blue"
        radius="sm"
      />
      {`${data?.fields?.first_name} ${data?.fields?.last_name}`}
    </Group>
  );
}
