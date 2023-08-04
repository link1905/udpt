import {
  Box,
  Button,
  Input,
  List,
  Paper,
  Select,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { DetailEditor } from "../../components/create-question-form/detail-editor";
import { UploadImage } from "../../components/create-question-form/upload-image";
import { TagsInput } from "../../components/create-question-form/tags-input";
import { NavLink } from "react-router-dom";

export function CreateQuestionPage() {
  return (
    <Box pb={100}>
      <Title mb="xl">Ask a question</Title>
      <Stack spacing="lg">
        <Paper withBorder p="xl">
          <Title order={4}>Writing a good question</Title>
          <Text fz="sm">
            You’re ready to ask a programming-related question and this form
            will help guide you through the process. Looking to ask a
            non-programming question? See the topics here to find a relevant
            site.
          </Text>
          <br />
          <Text fz="sm" fw="bold">
            Steps
          </Text>
          <List>
            <List.Item fz="sm">
              Summarize your problem in a one-line title.
            </List.Item>
            <List.Item fz="sm">Describe your problem in more detail.</List.Item>
            <List.Item fz="sm">
              Describe what you tried and what you expected to happen.
            </List.Item>
            <List.Item fz="sm">
              Add “tags” which help surface your question to members of the
              community.
            </List.Item>
            <List.Item fz="sm">
              Review your question and post it to the site
            </List.Item>
          </List>
        </Paper>
        <Paper withBorder p="xl">
          <Input.Wrapper
            mb="md"
            withAsterisk
            label="Title"
            description="Be specific and imagine you’re asking a question to another person."
          >
            <Input placeholder="e.g. Is there an R function for finding the index of an element in a vector?" />
          </Input.Wrapper>
        </Paper>
        <Paper withBorder p="xl">
          <Input.Wrapper
            mb="md"
            withAsterisk
            label="What are the details of your problem?"
            description="Introduce the problem and expand on what you put in the title. Minimum 20 characters."
          >
            <Box mt="sm">
              <DetailEditor />
            </Box>
          </Input.Wrapper>
        </Paper>
        <Paper withBorder p="xl">
          <Input.Wrapper
            mb="md"
            withAsterisk
            label="Attach some demo images"
            description="Attach some demo images"
          >
            <Box mt="sm">
              <UploadImage />
            </Box>
          </Input.Wrapper>
        </Paper>
        <Paper withBorder p="xl">
          <Input.Wrapper
            mb="md"
            withAsterisk
            label="Tags"
            description="Add up to 5 tags to describe what your question is about. Start typing to see suggestions."
          >
            <Box mt="sm">
              <TagsInput />
            </Box>
          </Input.Wrapper>
        </Paper>
        <Paper withBorder p="xl">
          <Input.Wrapper
            mb="md"
            withAsterisk
            label="Category"
            description="Select a category"
          >
            <Box mt="sm">
              <Select
                placeholder="Pick one"
                data={[
                  { value: "react", label: "React" },
                  { value: "ng", label: "Angular" },
                  { value: "svelte", label: "Svelte" },
                  { value: "vue", label: "Vue" },
                ]}
              />
            </Box>
          </Input.Wrapper>
        </Paper>
        <Box>
          <NavLink to={"/question/id"}>
            <Button>Submit question</Button>
          </NavLink>
        </Box>
      </Stack>
    </Box>
  );
}
