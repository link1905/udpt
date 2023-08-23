import { Box, Button, Group, Paper, TextInput, Title } from "@mantine/core";
import { DetailEditor } from "../create-question-form/detail-editor";
import { useForm } from "@mantine/form";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { requestCreateThread } from "../../services/forum/create-thread.ts";
import { getThreadQueryKey } from "../../services/forum/get-thread.ts";

export function AnswerForm({
  id,
  title,
}: {
  id: string | number;
  title: string;
}) {
  const queryClient = useQueryClient();
  const form = useForm({
    initialValues: {
      content: "",
      title: "",
    },
    validate: {
      title: (value) => !value,
      content: (value) => !value,
    },
  });

  const { mutate, isLoading } = useMutation(requestCreateThread, {
    onSuccess() {
      return queryClient.invalidateQueries(getThreadQueryKey(id));
    },
  });

  const handleSubmit = (values: { content: string; title: string }) => {
    mutate({
      ...values,
      parent: Number(id),
    });
  };

  return (
    <Box component="form" onSubmit={form.onSubmit(handleSubmit)}>
      <Title mb="md" order={4}>
        {title}
      </Title>
      <TextInput
        mb="md"
        title="Title"
        placeholder="Title"
        {...form.getInputProps("title")}
      />
      <DetailEditor {...form.getInputProps("content")} />
      <Group mt="md">
        <Button type="submit" loading={isLoading}>
          SUBMIT
        </Button>
      </Group>
    </Box>
  );
}
