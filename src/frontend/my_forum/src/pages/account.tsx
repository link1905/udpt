import {
  Grid,
  Group,
  Stack,
  TextInput,
  Button,
  Box,
  LoadingOverlay,
  Avatar,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  authRequestQueryKey,
  requestAuthRefresh,
} from "../services/account/auth-refresh.ts";
import { requestUpdateAccount } from "../services/account/update-account.ts";
import { useRef } from "react";

export interface AccountFormData {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password1: string;
  password2: string;
}

export function AccountPage() {
  const inputRef = useRef<HTMLInputElement>(null);
  const queryClient = useQueryClient();
  const { mutate, isLoading: isUpdating } = useMutation(requestUpdateAccount, {
    async onSuccess() {
      await queryClient.invalidateQueries(authRequestQueryKey);
    },
  });
  const { data, isLoading } = useQuery(
    authRequestQueryKey,
    requestAuthRefresh,
    {
      retry: 0,
    },
  );
  const form = useForm<AccountFormData>({
    initialValues: {
      username: data?.fields?.username ?? "",
      email: data?.fields?.email ?? "",
      first_name: data?.fields?.first_name ?? "",
      last_name: data?.fields?.last_name ?? "",
      password1: "",
      password2: "",
    },
    validate: {
      username: (value) => !value,
      email: (value) => !value,
      first_name: (value) => !value,
      last_name: (value) => !value,
    },
  });

  function handleSubmit(values: AccountFormData) {
    mutate({
      id: data?.pk ?? 0,
      ...values,
    });
  }

  return (
    <Box>
      <LoadingOverlay visible={isLoading} />
      <Grid>
        <Grid.Col span={3} sx={{ textAlign: "center" }}>
          <Group position="center">
            <input
              type="file"
              accept="image/png, image/gif, image/jpeg"
              ref={inputRef}
              style={{ display: "none" }}
              onChange={(e) => {
                mutate({
                  id: data?.pk ?? 0,
                  username: data?.fields?.username ?? "",
                  avatar: e.target?.files?.[0],
                });
              }}
            />
            <Avatar
              src={data?.fields?.avatar}
              sx={{ width: 200, height: 200 }}
              onClick={() => inputRef.current?.click()}
            />
          </Group>
        </Grid.Col>
        <Grid.Col span={9}>
          <form onSubmit={form.onSubmit(handleSubmit)}>
            <Stack>
              <TextInput
                placeholder="Username"
                label="Username"
                disabled
                {...form.getInputProps("username")}
              />
              <Group grow>
                <TextInput
                  placeholder="First name"
                  label="First name"
                  withAsterisk
                  {...form.getInputProps("first_name")}
                />
                <TextInput
                  placeholder="Last name"
                  label="Last name"
                  withAsterisk
                  {...form.getInputProps("last_name")}
                />
              </Group>
              <TextInput
                placeholder="Email"
                label="Email"
                withAsterisk
                {...form.getInputProps("email")}
              />
              <TextInput
                placeholder="Password"
                label="Password"
                {...form.getInputProps("password1")}
              />
              <TextInput
                placeholder="Confirm password"
                label="Confirm password"
                {...form.getInputProps("password2")}
              />
              <Group>
                <Button loading={isUpdating} type="submit">
                  Submit
                </Button>
              </Group>
            </Stack>
          </form>
        </Grid.Col>
      </Grid>
    </Box>
  );
}
