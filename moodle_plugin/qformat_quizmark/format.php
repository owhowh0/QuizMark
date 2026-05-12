<?php

defined('MOODLE_INTERNAL') || die();

require_once($CFG->dirroot . '/question/format.php');

class qformat_quizmark extends qformat_default {
    public function provide_import() {
        return true;
    }

    public function provide_export() {
        return false;
    }

    public function readquestions($lines) {
        $text = implode("\n", $lines);
        $parser = new quizmark_parser();
        $quiz = $parser->parse($text);
        return $this->build_questions($quiz);
    }

    private function build_questions($quiz) {
        $questions = array();
        foreach ($quiz['questions'] as $q) {
            $question = new stdClass();
            $question->qtype = 'multichoice';
            $question->name = $q['text'];
            $question->questiontext = $this->render_html($q['text'], $q['media'], $quiz['media']);
            $question->questiontextformat = FORMAT_HTML;
            $question->generalfeedback = '';
            $question->generalfeedbackformat = FORMAT_HTML;
            $question->correctfeedback = array('text' => '', 'format' => FORMAT_HTML);
            $question->partiallycorrectfeedback = array('text' => '', 'format' => FORMAT_HTML);
            $question->incorrectfeedback = array('text' => '', 'format' => FORMAT_HTML);
            $question->defaultgrade = $q['points'] !== null ? $q['points'] : 1;
            $question->single = 1;
            $question->shuffleanswers = 1;
            $question->answernumbering = 'abc';
            $question->shownumcorrect = 0;
            $question->answer = array();
            $question->fraction = array();
            $question->feedback = array();

            foreach ($q['answers'] as $a) {
                $answertext = $this->render_html($a['text'], $a['media'], array());
                $question->answer[] = array(
                    'text' => $answertext,
                    'format' => FORMAT_HTML,
                );
                $question->fraction[] = $a['correct'] ? 1.0 : 0.0;
                $question->feedback[] = array(
                    'text' => '',
                    'format' => FORMAT_HTML,
                );
            }

            $questions[] = $question;
        }
        return $questions;
    }

    private function render_html($text, $media, $quizmedia) {
        $parts = array();
        if ($text !== null && $text !== '') {
            $parts[] = htmlspecialchars($text, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
        }
        foreach ($quizmedia as $m) {
            $parts[] = $this->media_html($m);
        }
        foreach ($media as $m) {
            $parts[] = $this->media_html($m);
        }
        return implode('<br>', array_filter($parts));
    }

    private function media_html($media) {
        $value = htmlspecialchars($media['value'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
        switch ($media['kind']) {
            case 'image':
                return '<img src="' . $value . '" alt="Image">';
            case 'audio':
                return '<audio controls src="' . $value . '"></audio>';
            case 'video':
                return '<video controls src="' . $value . '"></video>';
            case 'attachment':
                return '<a href="' . $value . '">Attachment</a>';
            case 'math':
                return '\\(' . $value . '\\)';
            default:
                return $value;
        }
    }
}

class quizmark_parser {
    private $lines = array();
    private $index = 0;

    public function parse($text) {
        $raw = preg_split('/\r\n|\r|\n/', $text);
        $this->lines = array();
        foreach ($raw as $line) {
            $this->lines[] = rtrim($line, "\n");
        }
        $this->index = 0;

        $quizline = $this->next_nonempty();
        if ($quizline === null || stripos($quizline, 'QUIZ:') !== 0) {
            throw new moodle_exception('Invalid QUIZ header');
        }
        $title = trim(substr($quizline, 5));

        $quiz = array(
            'title' => $title,
            'media' => array(),
            'questions' => array(),
        );

        while (true) {
            $line = $this->peek_nonempty();
            if ($line === null) {
                break;
            }
            $trim = trim($line);
            if (stripos($trim, 'QUESTION') === 0) {
                break;
            }
            if (stripos($trim, 'THEME') === 0) {
                $this->consume_theme();
                continue;
            }
            if ($this->is_media_line($trim)) {
                $this->next_nonempty();
                $quiz['media'][] = $this->parse_media_line($trim);
                continue;
            }
            // Metadata lines are ignored for import.
            $this->next_nonempty();
        }

        while (true) {
            $line = $this->peek_nonempty();
            if ($line === null) {
                break;
            }
            $trim = trim($line);
            if (stripos($trim, 'QUESTION') !== 0) {
                throw new moodle_exception('Expected QUESTION block');
            }
            $quiz['questions'][] = $this->parse_question();
        }

        return $quiz;
    }

    private function parse_question() {
        $line = $this->next_nonempty();
        $matches = array();
        if (!preg_match('/^QUESTION\s*(?:\(([^)]*)\))?\s*:\s*(.*)$/i', $line, $matches)) {
            throw new moodle_exception('Invalid QUESTION syntax');
        }
        $points = null;
        if (!empty($matches[1])) {
            $parts = explode(',', $matches[1]);
            foreach ($parts as $part) {
                $part = trim($part);
                if (stripos($part, 'points=') === 0) {
                    $points = (float) substr($part, 7);
                }
            }
        }
        $text = trim($matches[2]);

        $question = array(
            'text' => $text,
            'points' => $points,
            'media' => array(),
            'answers' => array(),
        );

        while (true) {
            $line = $this->peek_nonempty();
            if ($line === null) {
                break;
            }
            $trim = trim($line);
            if ($this->is_answer_line($trim) || stripos($trim, 'QUESTION') === 0) {
                break;
            }
            $this->next_nonempty();
            if ($this->is_media_line($trim)) {
                $question['media'][] = $this->parse_media_line($trim);
                continue;
            }
        }

        while (true) {
            $line = $this->peek_nonempty();
            if ($line === null || stripos(trim($line), 'QUESTION') === 0) {
                break;
            }
            $trim = trim($line);
            if (!$this->is_answer_line($trim)) {
                throw new moodle_exception('Expected answer label');
            }
            $question['answers'][] = $this->parse_answer();
        }

        return $question;
    }

    private function parse_answer() {
        $line = $this->next_nonempty();
        $label = trim(substr($line, 0, strpos($line, ':')));
        $rest = trim(substr($line, strpos($line, ':') + 1));
        $correct = false;
        if (substr($rest, -1) === '*') {
            $correct = true;
            $rest = trim(substr($rest, 0, -1));
        }

        $text = null;
        $media = array();

        if ($rest !== '') {
            if ($this->is_media_line($rest)) {
                $media[] = $this->parse_media_line($rest);
            } else {
                $text = $rest;
            }
        } else {
            $next = $this->peek_nonempty();
            if ($next !== null) {
                $trim = trim($next);
                if ($this->is_media_line($trim)) {
                    $this->next_nonempty();
                    $media[] = $this->parse_media_line($trim);
                }
            }
        }

        while (true) {
            $next = $this->peek_nonempty();
            if ($next === null) {
                break;
            }
            $trim = trim($next);
            if (!$this->is_media_line($trim)) {
                break;
            }
            $this->next_nonempty();
            $media[] = $this->parse_media_line($trim);
        }

        return array(
            'label' => $label,
            'text' => $text,
            'media' => $media,
            'correct' => $correct,
        );
    }

    private function parse_media_line($line) {
        $parts = explode(':', $line, 2);
        $kind = strtolower(trim($parts[0]));
        $value = isset($parts[1]) ? trim($parts[1]) : '';
        if (substr($value, -1) === '*') {
            $value = trim(substr($value, 0, -1));
        }
        $value = $this->strip_quotes($value);
        return array('kind' => $this->normalize_kind($kind), 'value' => $value);
    }

    private function normalize_kind($kind) {
        $map = array(
            'image' => 'image',
            'audio' => 'audio',
            'video' => 'video',
            'attach' => 'attachment',
            'attachment' => 'attachment',
            'math' => 'math',
        );
        return isset($map[$kind]) ? $map[$kind] : $kind;
    }

    private function is_media_line($line) {
        $line = strtoupper($line);
        return strpos($line, 'IMAGE:') === 0 ||
            strpos($line, 'AUDIO:') === 0 ||
            strpos($line, 'VIDEO:') === 0 ||
            strpos($line, 'ATTACH:') === 0 ||
            strpos($line, 'MATH:') === 0;
    }

    private function is_answer_line($line) {
        return preg_match('/^[A-Z]\s*:/', $line) === 1;
    }

    private function consume_theme() {
        $line = $this->next_nonempty();
        if ($line === null) {
            return;
        }
        if (strpos($line, '{') !== false) {
            if (trim($line) === 'THEME {') {
                return $this->consume_theme_block();
            }
        }
        $next = $this->peek_nonempty();
        if ($next !== null && trim($next) === '{') {
            $this->next_nonempty();
            $this->consume_theme_block();
        }
    }

    private function consume_theme_block() {
        while (true) {
            $line = $this->next_nonempty();
            if ($line === null) {
                break;
            }
            if (trim($line) === '}') {
                break;
            }
        }
    }

    private function strip_quotes($value) {
        if (strlen($value) >= 2 && $value[0] === '"' && substr($value, -1) === '"') {
            return substr($value, 1, -1);
        }
        return $value;
    }

    private function next_nonempty() {
        while ($this->index < count($this->lines)) {
            $line = $this->lines[$this->index];
            $this->index++;
            $trim = trim($line);
            if ($trim === '' || strpos($trim, '#') === 0 || strpos($trim, '//') === 0) {
                continue;
            }
            return $line;
        }
        return null;
    }

    private function peek_nonempty() {
        $idx = $this->index;
        while ($idx < count($this->lines)) {
            $line = $this->lines[$idx];
            $trim = trim($line);
            if ($trim === '' || strpos($trim, '#') === 0 || strpos($trim, '//') === 0) {
                $idx++;
                continue;
            }
            return $line;
        }
        return null;
    }
}
